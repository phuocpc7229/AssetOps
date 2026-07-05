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

    def test_change_password_requires_authentication(self):
        response = self.client.post(
            "/api/v1/auth/change-password",
            {
                "current_password": "secure-password",
                "new_password": "new-secure-password",
                "confirm_password": "new-secure-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_change_password_rejects_incorrect_current_password(self):
        token = self.login_and_get_token()

        response = self.client.post(
            "/api/v1/auth/change-password",
            {
                "current_password": "wrong-password",
                "new_password": "new-secure-password",
                "confirm_password": "new-secure-password",
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["current_password"], ["Current password is incorrect."])

    def test_change_password_rejects_mismatched_confirmation(self):
        token = self.login_and_get_token()

        response = self.client.post(
            "/api/v1/auth/change-password",
            {
                "current_password": "secure-password",
                "new_password": "new-secure-password",
                "confirm_password": "different-secure-password",
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["confirm_password"], ["New password and confirmation do not match."])

    def test_change_password_rejects_short_new_password(self):
        token = self.login_and_get_token()

        response = self.client.post(
            "/api/v1/auth/change-password",
            {
                "current_password": "secure-password",
                "new_password": "short",
                "confirm_password": "short",
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("new_password", response.data)

    def test_change_password_updates_password_and_keeps_current_token_valid(self):
        token = self.login_and_get_token()

        response = self.client.post(
            "/api/v1/auth/change-password",
            {
                "current_password": "secure-password",
                "new_password": "new-secure-password",
                "confirm_password": "new-secure-password",
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "Password changed successfully.")

        old_login_response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )
        self.assertEqual(old_login_response.status_code, 401)

        new_login_response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "new-secure-password"},
            format="json",
        )
        self.assertEqual(new_login_response.status_code, 200)

        me_response = self.client.get("/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["user"]["username"], "admin")

    def login_and_get_token(self):
        login_response = self.client.post(
            "/api/v1/auth/login",
            {"username": "admin", "password": "secure-password"},
            format="json",
        )
        return login_response.data["access_token"]
