from django.test import TestCase
from rest_framework.test import APIClient


class HealthApiTests(TestCase):
    def test_health_endpoint(self):
        response = APIClient().get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "ok"})
        self.assertEqual(response["Content-Type"], "application/json")

    def test_cors_preflight_allows_authenticated_crud_methods_for_dev_origin(self):
        response = APIClient().options(
            "/api/v1/sites/5",
            HTTP_ORIGIN="http://127.0.0.1:5174",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="PATCH",
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS="authorization,content-type",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://127.0.0.1:5174")
        self.assertIn("PATCH", response["Access-Control-Allow-Methods"])
        self.assertIn("DELETE", response["Access-Control-Allow-Methods"])
        self.assertIn("authorization", response["Access-Control-Allow-Headers"])

    def test_cors_preflight_rejects_unlisted_origin(self):
        response = APIClient().options(
            "/api/v1/sites/5",
            HTTP_ORIGIN="http://evil.example",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="DELETE",
        )

        self.assertNotIn("Access-Control-Allow-Origin", response)

    def test_health_endpoint_uses_json_for_browser_accept_header(self):
        response = APIClient().get(
            "/api/v1/health",
            HTTP_ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "ok"})
        self.assertEqual(response["Content-Type"], "application/json")
