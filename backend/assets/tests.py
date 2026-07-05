from datetime import date, timedelta
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import AdminUser
from accounts.security import hash_password
from assets.models import Asset, AssetIPAddress, AssetType, DeviceType, Location, Vendor
from sites.models import Site


class AssetApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AdminUser.objects.create(
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
        self.token = login_response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.site = Site.objects.create(code="HQ", name="Headquarters", address="100 Operations Way")
        self.asset_type = AssetType.objects.create(code="NET", name="Network Device")
        self.vendor = Vendor.objects.create(code="CISCO", name="Cisco")
        self.location = Location.objects.create(code="MDF", name="MDF")

    def create_asset(self, **overrides):
        data = {
            "asset_tag": "ASSET-001",
            "name": "Core Router",
            "hostname": "core-router-01",
            "asset_type": self.asset_type,
            "vendor": self.vendor,
            "model": "ISR",
            "serial_number": "SN001",
            "ip_address": "10.10.0.1",
            "mac_address": "aa-bb-cc-dd-ee-ff",
            "site": self.site,
            "location": self.location,
            "status": Asset.Status.ACTIVE,
            "criticality": Asset.Criticality.CRITICAL,
            "warranty_starts_on": "2026-01-01",
            "warranty_expires_on": "2027-01-01",
            "purchase_date": "2026-01-15",
            "notes": "Primary edge device.",
        }
        data.update(overrides)
        return Asset.objects.create(**data, created_by=self.user, updated_by=self.user)

    def test_assets_require_authentication(self):
        client = APIClient()
        response = client.get("/api/v1/assets")

        self.assertEqual(response.status_code, 403)

    def test_create_asset_validates_and_normalizes_mac_address(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-001",
                "name": "Core Router",
                "hostname": "core-router-01",
                "asset_type_id": self.asset_type.id,
                "vendor_id": self.vendor.id,
                "serial_number": "SN001",
                "ip_address": "2001:db8::1",
                "mac_address": "aabb.ccdd.eeff",
                "site_id": self.site.id,
                "location_id": self.location.id,
                "criticality": "critical",
                "warranty_starts_on": "2026-01-01",
                "warranty_expires_on": "2027-01-01",
                "purchase_date": "2026-01-15",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["mac_address"], "AA:BB:CC:DD:EE:FF")
        self.assertEqual(response.data["asset_type"]["code"], "NET")
        self.assertEqual(response.data["vendor"]["name"], "Cisco")
        self.assertEqual(response.data["site"]["code"], "HQ")
        self.assertEqual(response.data["location"]["code"], "MDF")
        self.assertEqual(response.data["created_by"], self.user.id)
        self.assertEqual(response.data["updated_by"], self.user.id)
        self.assertEqual(response.data["ip_address"], "2001:db8::1")
        self.assertEqual(len(response.data["ip_addresses"]), 1)
        self.assertEqual(response.data["ip_addresses"][0]["address"], "2001:db8::1")
        self.assertTrue(response.data["ip_addresses"][0]["is_primary"])

    def test_create_asset_with_multiple_ip_addresses_sets_primary(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-010",
                "name": "Core Switch",
                "asset_type_id": self.asset_type.id,
                "site_id": self.site.id,
                "criticality": "high",
                "ip_addresses": [
                    {"address": "10.10.0.10", "is_primary": False},
                    {"address": "10.10.0.11", "is_primary": True},
                    {"address": "2001:db8::11", "is_primary": False},
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["ip_address"], "10.10.0.11")
        self.assertEqual(len(response.data["ip_addresses"]), 3)
        self.assertEqual(
            AssetIPAddress.objects.get(asset_id=response.data["id"], is_primary=True).address,
            "10.10.0.11",
        )

    def test_update_asset_replaces_ip_addresses_and_primary(self):
        asset = self.create_asset(ip_address="10.10.0.1")

        response = self.client.patch(
            f"/api/v1/assets/{asset.id}",
            {
                "ip_addresses": [
                    {"address": "10.20.0.1", "is_primary": False},
                    {"address": "10.20.0.2", "is_primary": True},
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["ip_address"], "10.20.0.2")
        self.assertEqual(len(response.data["ip_addresses"]), 2)
        self.assertEqual(set(asset.ip_addresses.values_list("address", flat=True)), {"10.20.0.1", "10.20.0.2"})

    def test_create_asset_rejects_duplicate_ip_addresses(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-011",
                "name": "Duplicate IP",
                "asset_type_id": self.asset_type.id,
                "site_id": self.site.id,
                "criticality": "medium",
                "ip_addresses": [
                    {"address": "10.10.0.20", "is_primary": True},
                    {"address": "10.10.0.20", "is_primary": False},
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ip_addresses", response.data)

    def test_create_asset_rejects_invalid_nested_ip_address(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-012",
                "name": "Invalid IP",
                "asset_type_id": self.asset_type.id,
                "site_id": self.site.id,
                "criticality": "medium",
                "ip_addresses": [{"address": "not-an-ip", "is_primary": True}],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ip_addresses", response.data)

    def test_create_rejects_duplicate_asset_tag(self):
        self.create_asset()

        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-001",
                "name": "Duplicate",
                "asset_type_id": self.asset_type.id,
                "site_id": self.site.id,
                "criticality": "medium",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("asset_tag", response.data)

    def test_create_rejects_duplicate_non_empty_serial_number(self):
        self.create_asset(serial_number="SERIAL-1")

        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-002",
                "name": "Duplicate Serial",
                "asset_type_id": self.asset_type.id,
                "serial_number": "SERIAL-1",
                "site_id": self.site.id,
                "criticality": "medium",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("serial_number", response.data)

    def test_allows_multiple_empty_serial_numbers(self):
        self.create_asset(asset_tag="ASSET-001", serial_number="")

        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-002",
                "name": "No Serial",
                "asset_type_id": self.asset_type.id,
                "serial_number": "",
                "site_id": self.site.id,
                "criticality": "low",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_validation_rejects_invalid_ip_and_mac(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-001",
                "name": "Invalid Asset",
                "asset_type_id": self.asset_type.id,
                "ip_address": "not-an-ip",
                "mac_address": "not-a-mac",
                "site_id": self.site.id,
                "criticality": "medium",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ip_address", response.data)
        self.assertIn("mac_address", response.data)

    def test_validation_rejects_invalid_dates(self):
        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-001",
                "name": "Invalid Dates",
                "asset_type_id": self.asset_type.id,
                "site_id": self.site.id,
                "criticality": "medium",
                "warranty_starts_on": "2026-06-01",
                "warranty_expires_on": "2026-05-01",
                "purchase_date": (date.today() + timedelta(days=1)).isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("warranty_expires_on", response.data)
        self.assertIn("purchase_date", response.data)

    def test_create_rejects_soft_deleted_site(self):
        deleted_site = Site.objects.create(
            code="OLD",
            name="Old Campus",
            address="300 Retired Road",
            is_deleted=True,
        )

        response = self.client.post(
            "/api/v1/assets",
            {
                "asset_tag": "ASSET-001",
                "name": "Core Router",
                "asset_type_id": self.asset_type.id,
                "site_id": deleted_site.id,
                "criticality": "medium",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["site_id"], ["Selected site does not exist or has been deleted."])

    def test_update_rejects_soft_deleted_site(self):
        asset = self.create_asset()
        deleted_site = Site.objects.create(
            code="OLD",
            name="Old Campus",
            address="300 Retired Road",
            is_deleted=True,
        )

        response = self.client.patch(
            f"/api/v1/assets/{asset.id}",
            {"site_id": deleted_site.id},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["site_id"], ["Selected site does not exist or has been deleted."])

    def test_list_excludes_archived_by_default_and_can_include_archived(self):
        active_asset = self.create_asset(asset_tag="ASSET-001", serial_number="SN001")
        archived_asset = self.create_asset(
            asset_tag="ASSET-002",
            name="Archived Laptop",
            serial_number="SN002",
            status=Asset.Status.ARCHIVED,
        )

        response = self.client.get("/api/v1/assets")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], active_asset.id)

        response = self.client.get("/api/v1/assets?include_archived=true")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual({item["id"] for item in response.data["results"]}, {active_asset.id, archived_asset.id})

    def test_search_filters_pagination_and_ordering(self):
        self.create_asset(
            asset_tag="ASSET-001",
            name="Core Router",
            hostname="core-router-01",
            serial_number="SN001",
            vendor=self.vendor,
            site=self.site,
            criticality=Asset.Criticality.CRITICAL,
            ip_address="10.10.0.1",
        )
        data_center = Site.objects.create(code="DC", name="Data Center", address="200 Data Center Road")
        server_type = AssetType.objects.create(code="SERVER", name="Server")
        dell = Vendor.objects.create(code="DELL", name="Dell")
        self.create_asset(
            asset_tag="ASSET-002",
            name="Database Server",
            hostname="db-01",
            serial_number="SN002",
            vendor=dell,
            site=data_center,
            asset_type=server_type,
            criticality=Asset.Criticality.HIGH,
            ip_address="10.10.0.2",
        )
        self.create_asset(
            asset_tag="ASSET-003",
            name="Archive Server",
            hostname="archive-01",
            serial_number="SN003",
            vendor=dell,
            site=data_center,
            asset_type=server_type,
            criticality=Asset.Criticality.LOW,
            ip_address="10.10.0.3",
        )

        response = self.client.get(
            f"/api/v1/assets?search=server&vendor={dell.id}&asset_type={server_type.id}&site={data_center.id}&ordering=-asset_tag&page=1&page_size=1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(response.data["page_size"], 1)
        self.assertEqual(response.data["total_pages"], 2)
        self.assertEqual(response.data["results"][0]["asset_tag"], "ASSET-003")

    def test_detail_patch_and_soft_archive(self):
        asset = self.create_asset()

        detail_response = self.client.get(f"/api/v1/assets/{asset.id}")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["asset_tag"], "ASSET-001")
        self.assertEqual(detail_response.data["asset_type"]["name"], "Network Device")
        self.assertEqual(detail_response.data["site"]["name"], "Headquarters")

        patch_response = self.client.patch(
            f"/api/v1/assets/{asset.id}",
            {"hostname": "core-router-02", "mac_address": "11:22:33:44:55:66"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data["hostname"], "core-router-02")
        self.assertEqual(patch_response.data["mac_address"], "11:22:33:44:55:66")
        self.assertEqual(patch_response.data["updated_by"], self.user.id)

        delete_response = self.client.delete(f"/api/v1/assets/{asset.id}")
        self.assertEqual(delete_response.status_code, 204)

        asset.refresh_from_db()
        self.assertEqual(asset.status, Asset.Status.ARCHIVED)

    @patch("assets.views.subprocess.run")
    def test_ping_asset_with_ip_address(self, run_mock):
        run_mock.return_value = Mock(returncode=0, stdout="Reply from 10.10.0.1: time=12ms", stderr="")
        asset = self.create_asset(ip_address="10.10.0.1")

        response = self.client.post(f"/api/v1/assets/{asset.id}/ping", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["ip_address"], "10.10.0.1")
        self.assertEqual(response.data["latency_ms"], 12.0)
        self.assertEqual(response.data["message"], "Ping successful.")
        ping_call = run_mock.call_args
        self.assertFalse(ping_call.kwargs["shell"])
        self.assertIn("10.10.0.1", ping_call.args[0])

    @patch("assets.views.subprocess.run")
    def test_ping_asset_allows_selecting_stored_ip_address(self, run_mock):
        run_mock.return_value = Mock(returncode=0, stdout="Reply from 10.10.0.2: time=5ms", stderr="")
        asset = self.create_asset(ip_address="10.10.0.1")
        AssetIPAddress.objects.create(asset=asset, address="10.10.0.1", is_primary=True)
        AssetIPAddress.objects.create(asset=asset, address="10.10.0.2", is_primary=False)

        response = self.client.post(
            f"/api/v1/assets/{asset.id}/ping",
            {"ip_address": "10.10.0.2"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["ip_address"], "10.10.0.2")
        self.assertIn("10.10.0.2", run_mock.call_args.args[0])

    def test_ping_rejects_ip_address_not_assigned_to_asset(self):
        asset = self.create_asset(ip_address="10.10.0.1")
        AssetIPAddress.objects.create(asset=asset, address="10.10.0.1", is_primary=True)

        response = self.client.post(
            f"/api/v1/assets/{asset.id}/ping",
            {"ip_address": "10.10.0.99"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Selected IP address does not belong to this asset.")

    def test_ping_requires_ip_address(self):
        asset = self.create_asset(ip_address=None)

        response = self.client.post(f"/api/v1/assets/{asset.id}/ping", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Ping test requires an asset IP address.")


class MasterDataApiTests(TestCase):
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

    def assert_master_data_crud(self, endpoint, model, expected_code):
        response = self.client.post(
            endpoint,
            {"name": "Core", "description": "Primary records"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["code"], expected_code)
        item_id = response.data["id"]

        duplicate_response = self.client.post(
            endpoint,
            {"code": expected_code.lower(), "name": "Duplicate"},
            format="json",
        )
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(duplicate_response.data["code"], ["A record with this code already exists."])

        list_response = self.client.get(f"{endpoint}?search=pri&page=1&page_size=1")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(list_response.data["page_size"], 1)

        patch_response = self.client.patch(f"{endpoint}/{item_id}", {"name": "Core Updated"}, format="json")
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data["name"], "Core Updated")

        delete_response = self.client.delete(f"{endpoint}/{item_id}")
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(model.objects.active().filter(pk=item_id).exists())
        self.assertTrue(model.objects.filter(pk=item_id, is_deleted=True).exists())

        hidden_response = self.client.get(endpoint)
        self.assertEqual(hidden_response.status_code, 200)
        self.assertEqual(hidden_response.data["count"], 0)

        included_response = self.client.get(f"{endpoint}?include_deleted=true")
        self.assertEqual(included_response.status_code, 200)
        self.assertEqual(included_response.data["count"], 1)

    def assert_master_data_generates_unique_code_suffix(self, endpoint, expected_first_code, expected_second_code):
        first_response = self.client.post(
            endpoint,
            {"name": "Network Switch", "description": "Switches"},
            format="json",
        )
        second_response = self.client.post(
            endpoint,
            {"name": "Network Switch", "description": "More switches"},
            format="json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        self.assertEqual(first_response.data["code"], expected_first_code)
        self.assertEqual(second_response.data["code"], expected_second_code)

    def assert_master_data_update_rejects_normalized_duplicate_code(self, endpoint, model):
        model.objects.create(code="ABC", name="Existing")
        item = model.objects.create(code="DEF", name="Updated")

        response = self.client.patch(f"{endpoint}/{item.id}", {"code": "abc"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], ["A record with this code already exists."])

    def test_asset_type_crud_search_pagination_and_soft_delete(self):
        self.assert_master_data_crud("/api/v1/asset-types", AssetType, "CORE")
        self.assert_master_data_generates_unique_code_suffix(
            "/api/v1/asset-types",
            "SWITCH",
            "SWITCH-02",
        )

    def test_vendor_crud_search_pagination_and_soft_delete(self):
        self.assert_master_data_crud("/api/v1/vendors", Vendor, "CORE")
        self.assert_master_data_generates_unique_code_suffix(
            "/api/v1/vendors",
            "NETWORK-SWITCH",
            "NETWORK-SWITCH-02",
        )

    def test_device_type_crud_search_pagination_and_soft_delete(self):
        self.assert_master_data_crud("/api/v1/device-types", DeviceType, "CORE")
        self.assert_master_data_generates_unique_code_suffix(
            "/api/v1/device-types",
            "NETWORK-SWITCH",
            "NETWORK-SWITCH-02",
        )

    def test_location_crud_search_pagination_and_soft_delete(self):
        self.assert_master_data_crud("/api/v1/locations", Location, "CORE")
        self.assert_master_data_generates_unique_code_suffix(
            "/api/v1/locations",
            "NETWORK-SWITCH",
            "NETWORK-SWITCH-02",
        )

    def test_asset_type_update_rejects_normalized_duplicate_code(self):
        self.assert_master_data_update_rejects_normalized_duplicate_code("/api/v1/asset-types", AssetType)

    def test_vendor_update_rejects_normalized_duplicate_code(self):
        self.assert_master_data_update_rejects_normalized_duplicate_code("/api/v1/vendors", Vendor)

    def test_device_type_update_rejects_normalized_duplicate_code(self):
        self.assert_master_data_update_rejects_normalized_duplicate_code("/api/v1/device-types", DeviceType)

    def test_location_update_rejects_normalized_duplicate_code(self):
        self.assert_master_data_update_rejects_normalized_duplicate_code("/api/v1/locations", Location)


class SeedMasterDataCommandTests(TestCase):
    def test_seed_master_data_creates_defaults(self):
        call_command("seed_master_data")

        self.assertTrue(AssetType.objects.filter(code="SERVER", name="Server").exists())
        self.assertTrue(AssetType.objects.filter(code="SWITCH", name="Network Switch").exists())
        self.assertTrue(Vendor.objects.filter(code="CISCO", name="Cisco").exists())
        self.assertTrue(Vendor.objects.filter(code="HUAWEI", name="Huawei").exists())
        self.assertTrue(DeviceType.objects.filter(code="CORE-SW", name="Core Switch").exists())
        self.assertTrue(DeviceType.objects.filter(code="RACK-SRV", name="Rack Server").exists())
        self.assertTrue(Location.objects.filter(code="SRV-ROOM", name="Server Room").exists())
        self.assertTrue(Location.objects.filter(code="RACK-A01", name="Rack A01").exists())

    def test_seed_master_data_is_idempotent_and_preserves_existing_records(self):
        Location.objects.create(code="SRV-ROOM", name="Existing Server Room", description="Keep this")

        call_command("seed_master_data")
        first_counts = {
            "asset_types": AssetType.objects.count(),
            "vendors": Vendor.objects.count(),
            "device_types": DeviceType.objects.count(),
            "locations": Location.objects.count(),
        }
        call_command("seed_master_data")

        self.assertEqual(AssetType.objects.count(), first_counts["asset_types"])
        self.assertEqual(Vendor.objects.count(), first_counts["vendors"])
        self.assertEqual(DeviceType.objects.count(), first_counts["device_types"])
        self.assertEqual(Location.objects.count(), first_counts["locations"])
        self.assertEqual(Location.objects.get(code="SRV-ROOM").name, "Existing Server Room")
        self.assertEqual(Location.objects.get(code="SRV-ROOM").description, "Keep this")
