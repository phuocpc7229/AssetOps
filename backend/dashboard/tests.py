from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import AdminUser
from accounts.security import hash_password
from assets.models import Asset, AssetIPAddress, AssetType, DeviceType, Location, Vendor
from sites.models import Site


class DashboardApiTests(TestCase):
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

        self.site = Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")
        self.branch = Site.objects.create(code="BR", name="Branch", address="200 Operations Way")
        self.server_type = AssetType.objects.create(code="SERVER", name="Server")
        self.switch_type = AssetType.objects.create(code="SWITCH", name="Network Switch")
        self.vendor = Vendor.objects.create(code="CISCO", name="Cisco")
        self.location = Location.objects.create(code="MDF", name="Main Distribution Frame")
        self.device_type = DeviceType.objects.create(code="CORE-SW", name="Core Switch")
        self.today = timezone.localdate()

    def test_dashboard_endpoints_require_authentication(self):
        client = APIClient()

        for path in [
            "/api/v1/dashboard/metrics",
            "/api/v1/dashboard/recent-assets",
            "/api/v1/dashboard/recent-activity",
        ]:
            response = client.get(path)
            self.assertEqual(response.status_code, 403)

    def test_metrics_returns_kpi_array_charts_and_quick_action_badges(self):
        self.create_asset(
            asset_tag="AT-1001",
            name="Core Router",
            status=Asset.Status.ACTIVE,
            criticality=Asset.Criticality.HIGH,
            ip_address="10.0.0.1",
            warranty_expires_on=self.today + timedelta(days=220),
            asset_type=self.switch_type,
        )
        self.create_asset(
            asset_tag="AT-1002",
            name="Storage Controller",
            status=Asset.Status.IN_MAINTENANCE,
            criticality=Asset.Criticality.CRITICAL,
            ip_address="10.0.0.2",
            warranty_expires_on=self.today + timedelta(days=10),
            asset_type=self.server_type,
        )
        self.create_asset(
            asset_tag="AT-1003",
            name="Retired Firewall",
            status=Asset.Status.ARCHIVED,
            criticality=Asset.Criticality.MEDIUM,
            ip_address="10.0.0.3",
            warranty_expires_on=self.today - timedelta(days=15),
            asset_type=self.switch_type,
        )
        self.create_asset(
            asset_tag="AT-1004",
            name="Unassigned Workstation",
            status=Asset.Status.ACTIVE,
            criticality=Asset.Criticality.LOW,
            warranty_expires_on=None,
            asset_type=self.server_type,
        )

        response = self.client.get("/api/v1/dashboard/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertIn("generated_at", response.data)
        self.assertEqual(
            [item["key"] for item in response.data["kpis"]],
            [
                "total_assets",
                "active_assets",
                "maintenance_assets",
                "expiring_warranty",
                "online_assets",
            ],
        )
        values_by_key = {item["key"]: item["value"] for item in response.data["kpis"]}
        self.assertEqual(values_by_key["total_assets"], 4)
        self.assertEqual(values_by_key["active_assets"], 2)
        self.assertEqual(values_by_key["maintenance_assets"], 1)
        self.assertEqual(values_by_key["expiring_warranty"], 1)
        self.assertEqual(values_by_key["online_assets"], 2)
        self.assertEqual(len(response.data["kpis"][0]["trend"]), 14)
        self.assertEqual(response.data["charts"]["assets_by_type"]["total"], 3)
        self.assertEqual(response.data["charts"]["warranty_status"]["total"], 3)
        self.assertEqual(response.data["quick_action_badges"]["archived_assets"], 1)
        self.assertEqual(response.data["quick_action_badges"]["maintenance_assets"], 1)
        self.assertEqual(response.data["quick_action_badges"]["expiring_warranty"], 1)

    def test_recent_assets_returns_compact_contract_and_respects_limit(self):
        first_asset = self.create_asset(
            asset_tag="AT-2001",
            name="Older Asset",
            status=Asset.Status.ACTIVE,
            ip_address="10.1.0.1",
            asset_type=self.server_type,
        )
        latest_asset = self.create_asset(
            asset_tag="AT-2002",
            name="Latest Asset",
            status=Asset.Status.IN_MAINTENANCE,
            criticality=Asset.Criticality.CRITICAL,
            ip_address="10.1.0.2",
            asset_type=self.switch_type,
            site=self.branch,
        )
        AssetIPAddress.objects.create(asset=latest_asset, address="10.1.0.20", is_primary=False)
        Asset.objects.filter(pk=first_asset.pk).update(updated_at=timezone.now() - timedelta(days=1))
        Asset.objects.filter(pk=latest_asset.pk).update(updated_at=timezone.now())

        response = self.client.get("/api/v1/dashboard/recent-assets?limit=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        result = response.data["results"][0]
        self.assertEqual(result["asset_tag"], "AT-2002")
        self.assertEqual(result["primary_ip"], "10.1.0.2")
        self.assertEqual(result["ip_count"], 2)
        self.assertEqual(result["asset_type"], {"id": self.switch_type.id, "code": "SWITCH", "name": "Network Switch"})
        self.assertEqual(result["site"], {"id": self.branch.id, "code": "BR", "name": "Branch"})
        self.assertEqual(result["warranty_state"], "unknown")
        self.assertNotIn("notes", result)

    def test_recent_activity_is_marked_as_temporary_inferred_activity(self):
        asset = self.create_asset(
            asset_tag="AT-3001",
            name="Archived Asset",
            status=Asset.Status.ARCHIVED,
            ip_address="10.3.0.1",
            asset_type=self.server_type,
        )
        Site.objects.filter(pk=self.site.pk).update(updated_at=timezone.now() - timedelta(minutes=10))
        Asset.objects.filter(pk=asset.pk).update(updated_at=timezone.now())

        response = self.client.get("/api/v1/dashboard/recent-activity?limit=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["source"], "temporary_inferred")
        self.assertIn("AuditEvent", response.data["note"])
        asset_activity = next(item for item in response.data["results"] if item["id"] == f"asset-{asset.id}")
        self.assertEqual(asset_activity["action"], "archived")
        self.assertEqual(asset_activity["entity_type"], "asset")
        self.assertEqual(asset_activity["severity"], "warning")
        self.assertEqual(asset_activity["route"], f"/dashboard/assets/{asset.id}/edit")

    def create_asset(
        self,
        asset_tag: str,
        name: str,
        status: str,
        asset_type: AssetType,
        criticality: str = Asset.Criticality.MEDIUM,
        ip_address: str | None = None,
        warranty_expires_on=None,
        site: Site | None = None,
    ) -> Asset:
        asset = Asset.objects.create(
            asset_tag=asset_tag,
            name=name,
            hostname=asset_tag.lower(),
            asset_type=asset_type,
            vendor=self.vendor,
            site=site or self.site,
            location=self.location,
            status=status,
            criticality=criticality,
            ip_address=ip_address,
            warranty_expires_on=warranty_expires_on,
        )
        if ip_address:
            AssetIPAddress.objects.create(asset=asset, address=ip_address, is_primary=True)
        return asset
