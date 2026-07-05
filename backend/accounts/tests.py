from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import AdminUser
from accounts.security import hash_password


class AuthenticationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AdminUser.objects.create(
            username="admin",
            password_hash=hash_password("secure-password"),
            is_active=True,
            is_superuser=True,
        )

    def test_login_returns_access_token_and_safe_user(self):
        response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertEqual(response.data["token_type"], "Bearer")
        self.assertEqual(response.data["user"]["username"], "admin")
        self.assertNotIn("password_hash", response.data["user"])

    def test_login_rejects_invalid_password(self):
        response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access_token", response.data)

    def test_login_rejects_inactive_user(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_me_requires_authentication(self):
        response = self.client.get("/api/v1/auth/me")

        self.assertEqual(response.status_code, 403)

    def test_me_returns_authenticated_user(self):
        login_response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )
        token = login_response.data["access_token"]

        response = self.client.get("/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["username"], "admin")
        self.assertNotIn("password_hash", response.data["user"])
