from django.test import TestCase
from rest_framework.test import APIClient


class HealthApiTests(TestCase):
    def test_health_endpoint(self):
        response = APIClient().get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "ok"})
        self.assertEqual(response["Content-Type"], "application/json")

    def test_health_endpoint_uses_json_for_browser_accept_header(self):
        response = APIClient().get(
            "/api/v1/health",
            HTTP_ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "ok"})
        self.assertEqual(response["Content-Type"], "application/json")
