import re
import unicodedata
from datetime import date

from rest_framework import serializers

from assets.models import Asset, AssetIPAddress, AssetType, DeviceType, Location, Vendor
from sites.models import Site


MAC_ADDRESS_PATTERN = re.compile(
    r"^[0-9A-Fa-f]{2}([-:])(?:[0-9A-Fa-f]{2}\1){4}[0-9A-Fa-f]{2}$"
    r"|^[0-9A-Fa-f]{4}(\.)(?:[0-9A-Fa-f]{4}\2){1}[0-9A-Fa-f]{4}$"
    r"|^[0-9A-Fa-f]{12}$"
)


def normalize_mac_address(value: str) -> str:
    if not value:
        return ""

    value = value.strip()
    if not MAC_ADDRESS_PATTERN.fullmatch(value):
        raise serializers.ValidationError("Enter a valid MAC address.")

    normalized = re.sub(r"[^0-9A-Fa-f]", "", value).upper()
    return ":".join(normalized[index : index + 2] for index in range(0, 12, 2))


def build_code_from_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().replace("Đ", "D").replace("đ", "d"))
    ascii_value = "".join(character for character in normalized if not unicodedata.combining(character))
    code = re.sub(r"[^0-9A-Za-z]+", "-", ascii_value.upper()).strip("-")
    return re.sub(r"-+", "-", code) or "RECORD"


def build_unique_code(model, prefix: str, name: str) -> str:
    base_code = f"{prefix}-{build_code_from_name(name)}"[:40]
    code = base_code
    suffix = 2

    while model.objects.filter(code=code).exists():
        suffix_text = f"-{suffix:02d}"
        code = f"{base_code[:40 - len(suffix_text)]}{suffix_text}"
        suffix += 1

    return code


def build_short_code_from_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().replace("\u0110", "D").replace("\u0111", "d"))
    ascii_value = "".join(character for character in normalized if not unicodedata.combining(character))
    code = re.sub(r"[^0-9A-Za-z]+", "-", ascii_value.upper()).strip("-")
    return re.sub(r"-+", "-", code) or "RECORD"


def build_unique_short_code(model, name: str, aliases: dict[str, str]) -> str:
    normalized_name = build_short_code_from_name(name)
    base_code = aliases.get(normalized_name, normalized_name)[:40]
    code = base_code
    suffix = 2

    while model.objects.filter(code=code).exists():
        suffix_text = f"-{suffix:02d}"
        code = f"{base_code[:40 - len(suffix_text)]}{suffix_text}"
        suffix += 1

    return code


class MasterDataSerializer(serializers.ModelSerializer):
    code_prefix = "REC"
    code_aliases: dict[str, str] = {}

    class Meta:
        fields = ["id", "code", "name", "description", "is_deleted", "deleted_at", "created_at", "updated_at"]
        read_only_fields = ["id", "is_deleted", "deleted_at", "created_at", "updated_at"]
        extra_kwargs = {
            "code": {"validators": [], "required": False, "allow_blank": True},
        }

    def validate_code(self, value):
        value = value.strip().upper()
        if not value:
            if self.instance is not None:
                raise serializers.ValidationError("Code is required.")
            return value
        existing = self.Meta.model.objects.filter(code=value)
        if self.instance is not None:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError("A record with this code already exists.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_description(self, value):
        return value.strip()

    def validate(self, attrs):
        if self.instance is None and not attrs.get("code"):
            name = attrs.get("name", "").strip()
            if name:
                attrs["code"] = build_unique_short_code(self.Meta.model, name, self.code_aliases)

        return attrs


class AssetTypeSerializer(MasterDataSerializer):
    code_prefix = "AT"
    code_aliases = {
        "NETWORK-SWITCH": "SWITCH",
        "ACCESS-POINT": "AP",
        "CCTV-CAMERA": "CAMERA",
    }

    class Meta(MasterDataSerializer.Meta):
        model = AssetType


class VendorSerializer(MasterDataSerializer):
    code_prefix = "VEN"

    class Meta(MasterDataSerializer.Meta):
        model = Vendor


class DeviceTypeSerializer(MasterDataSerializer):
    code_prefix = "DT"
    code_aliases = {
        "CORE-SWITCH": "CORE-SW",
        "ACCESS-SWITCH": "ACCESS-SW",
        "DISTRIBUTION-SWITCH": "DIST-SW",
        "RACK-SERVER": "RACK-SRV",
        "TOWER-SERVER": "TOWER-SRV",
        "WIRELESS-ACCESS-POINT": "WIFI-AP",
        "EDGE-FIREWALL": "EDGE-FW",
        "ACCESS-POINT": "AP",
    }

    class Meta(MasterDataSerializer.Meta):
        model = DeviceType


class LocationSerializer(MasterDataSerializer):
    code_prefix = "LOC"
    code_aliases = {
        "SERVER-ROOM": "SRV-ROOM",
        "MAIN-DISTRIBUTION-FRAME": "MDF",
        "INTERMEDIATE-DISTRIBUTION-FRAME": "IDF",
        "STORAGE-ROOM": "STORAGE",
    }

    class Meta(MasterDataSerializer.Meta):
        model = Location


class AssetIPAddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = AssetIPAddress
        fields = ["id", "address", "is_primary"]
        read_only_fields = ["id"]

    def validate_address(self, value):
        value = value.strip()
        if not value:
            return value

        return serializers.IPAddressField().run_validation(value)


class AssetSerializer(serializers.ModelSerializer):
    asset_type = AssetTypeSerializer(read_only=True)
    asset_type_id = serializers.PrimaryKeyRelatedField(
        source="asset_type",
        queryset=AssetType.objects.active(),
        write_only=True,
    )
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        source="vendor",
        queryset=Vendor.objects.active(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    site = serializers.SerializerMethodField()
    site_id = serializers.PrimaryKeyRelatedField(
        source="site",
        queryset=Site.objects.active(),
        required=False,
        allow_null=True,
        write_only=True,
        error_messages={
            "does_not_exist": "Selected site does not exist or has been deleted.",
            "incorrect_type": "Selected site does not exist or has been deleted.",
        },
    )
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source="location",
        queryset=Location.objects.active(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    ip_addresses = AssetIPAddressSerializer(many=True, required=False)

    class Meta:
        model = Asset
        fields = [
            "id",
            "asset_tag",
            "name",
            "hostname",
            "asset_type",
            "asset_type_id",
            "vendor",
            "vendor_id",
            "model",
            "serial_number",
            "ip_address",
            "ip_addresses",
            "mac_address",
            "site",
            "site_id",
            "location",
            "location_id",
            "status",
            "criticality",
            "warranty_starts_on",
            "warranty_expires_on",
            "purchase_date",
            "notes",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]

    def get_site(self, obj):
        if obj.site is None:
            return None

        return {
            "id": obj.site.id,
            "code": obj.site.code,
            "name": obj.site.name,
        }

    def validate_asset_tag(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Asset tag is required.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_serial_number(self, value):
        return value.strip()

    def validate_mac_address(self, value):
        return normalize_mac_address(value)

    def validate_ip_addresses(self, value):
        cleaned_items = []
        seen_addresses = set()
        primary_count = 0

        for item in value:
            address = str(item.get("address", "")).strip()
            if not address:
                continue

            if address in seen_addresses:
                raise serializers.ValidationError("Duplicate IP addresses are not allowed.")

            seen_addresses.add(address)
            is_primary = bool(item.get("is_primary", False))
            if is_primary:
                primary_count += 1

            cleaned_items.append({"address": address, "is_primary": is_primary})

        if primary_count > 1:
            raise serializers.ValidationError("Only one IP address can be primary.")

        if cleaned_items and primary_count == 0:
            cleaned_items[0]["is_primary"] = True

        return cleaned_items

    def validate(self, attrs):
        warranty_starts_on = attrs.get("warranty_starts_on", getattr(self.instance, "warranty_starts_on", None))
        warranty_expires_on = attrs.get("warranty_expires_on", getattr(self.instance, "warranty_expires_on", None))
        purchase_date = attrs.get("purchase_date", getattr(self.instance, "purchase_date", None))
        site = attrs.get("site", getattr(self.instance, "site", None))

        errors = {}

        if site is None:
            errors["site_id"] = "Site is required."

        if warranty_starts_on and warranty_expires_on and warranty_expires_on < warranty_starts_on:
            errors["warranty_expires_on"] = "Warranty expiry cannot be before warranty start."

        if purchase_date and purchase_date > date.today():
            errors["purchase_date"] = "Purchase date cannot be in the future."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        ip_addresses = validated_data.pop("ip_addresses", None)
        if ip_addresses is None and validated_data.get("ip_address"):
            ip_addresses = [{"address": validated_data["ip_address"], "is_primary": True}]

        validated_data["ip_address"] = self.get_primary_ip_address(ip_addresses)
        asset = super().create(validated_data)
        if ip_addresses is not None:
            self.sync_ip_addresses(asset, ip_addresses)
        return asset

    def update(self, instance, validated_data):
        ip_addresses = validated_data.pop("ip_addresses", None)
        if ip_addresses is not None:
            validated_data["ip_address"] = self.get_primary_ip_address(ip_addresses)
        elif "ip_address" in validated_data:
            ip_addresses = (
                [{"address": validated_data["ip_address"], "is_primary": True}]
                if validated_data["ip_address"]
                else []
            )

        asset = super().update(instance, validated_data)
        if ip_addresses is not None:
            self.sync_ip_addresses(asset, ip_addresses)
        return asset

    def get_primary_ip_address(self, ip_addresses):
        if not ip_addresses:
            return None

        primary = next((item for item in ip_addresses if item["is_primary"]), ip_addresses[0])
        return primary["address"]

    def sync_ip_addresses(self, asset, ip_addresses):
        asset.ip_addresses.all().delete()
        AssetIPAddress.objects.bulk_create(
            [
                AssetIPAddress(asset=asset, address=item["address"], is_primary=item["is_primary"])
                for item in ip_addresses
            ]
        )
