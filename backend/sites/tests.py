from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import AdminUser
from accounts.security import hash_password
from sites.models import Site


class SiteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        AdminUser.objects.create(
            username="admin",
            password_hash=hash_password("secure-password"),
            is_active=True,
            is_superuser=True,
        )
        login_response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}")

    def test_sites_require_authentication(self):
        client = APIClient()

        for method, path in [
            ("get", "/api/v1/sites"),
            ("post", "/api/v1/sites"),
            ("patch", "/api/v1/sites/1"),
            ("delete", "/api/v1/sites/1"),
        ]:
            response = getattr(client, method)(path, {}, format="json")
            self.assertEqual(response.status_code, 403)

    def test_create_and_search_site(self):
        create_response = self.client.post(
            "/api/v1/sites",
            {
                "name": "Headquarters",
                "address": "100 Operations Way",
                "notes": "Primary site",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.data["code"], "HEADQUARTERS")

        list_response = self.client.get("/api/v1/sites?search=head&page_size=10")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(list_response.data["results"][0]["name"], "Headquarters")

    def test_create_generates_unique_site_code_suffix(self):
        first_response = self.client.post(
            "/api/v1/sites",
            {"name": "Ho Chi Minh Head Office", "address": "1 Nguyen Hue"},
            format="json",
        )
        second_response = self.client.post(
            "/api/v1/sites",
            {"name": "Ho Chi Minh Head Office", "address": "2 Nguyen Hue"},
            format="json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        self.assertEqual(first_response.data["code"], "HCM-HQ")
        self.assertEqual(second_response.data["code"], "HCM-HQ-02")

    def test_create_generates_site_code_without_vietnamese_accents(self):
        response = self.client.post(
            "/api/v1/sites",
            {"name": "Đà Nẵng Office", "address": "1 Bach Dang"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], "DN-BR01")

    def test_successful_edit_site(self):
        site = Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")

        patch_response = self.client.patch(
            f"/api/v1/sites/{site.id}",
            {"code": "hq2", "name": "HQ Campus", "address": "200 Operations Way"},
            format="json",
        )

        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data["code"], "HQ2")
        self.assertEqual(patch_response.data["name"], "HQ Campus")
        site.refresh_from_db()
        self.assertEqual(site.code, "HQ2")

    def test_successful_soft_delete_site(self):
        site = Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")

        delete_response = self.client.delete(f"/api/v1/sites/{site.id}")

        self.assertEqual(delete_response.status_code, 204)
        site.refresh_from_db()
        self.assertTrue(site.is_deleted)
        self.assertIsNotNone(site.deleted_at)

    def test_deleted_sites_are_excluded_by_default(self):
        active_site = Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")
        deleted_site = Site.objects.create(
            code="DC",
            name="Data Center",
            address="200 Data Center Road",
            is_deleted=True,
        )

        response = self.client.get("/api/v1/sites")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], active_site.id)

        include_response = self.client.get("/api/v1/sites?include_deleted=true")
        self.assertEqual(include_response.status_code, 200)
        self.assertEqual(include_response.data["count"], 2)
        self.assertEqual({item["id"] for item in include_response.data["results"]}, {active_site.id, deleted_site.id})

    def test_detail_update_and_delete_do_not_find_deleted_sites(self):
        site = Site.objects.create(
            code="HQ",
            name="Headquarters",
            address="100 Operations Way",
            is_deleted=True,
        )

        self.assertEqual(self.client.get(f"/api/v1/sites/{site.id}").status_code, 404)
        self.assertEqual(self.client.patch(f"/api/v1/sites/{site.id}", {"name": "Updated"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(f"/api/v1/sites/{site.id}").status_code, 404)

    def test_rejects_duplicate_site_code_on_create(self):
        Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")

        response = self.client.post(
            "/api/v1/sites",
            {"code": "hq", "name": "Duplicate", "address": "200 Operations Way"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], ["A site with this code already exists."])

    def test_rejects_duplicate_site_code_on_update(self):
        Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")
        branch = Site.objects.create(code="BR", name="Branch", address="200 Operations Way")

        response = self.client.patch(f"/api/v1/sites/{branch.id}", {"code": "hq"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], ["A site with this code already exists."])

    def test_rejects_missing_site_address(self):
        response = self.client.post(
            "/api/v1/sites",
            {"code": "HQ", "name": "Headquarters", "address": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["address"], ["Site address is required."])
