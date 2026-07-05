import re
from datetime import date

from rest_framework import serializers

from assets.models import Asset, AssetType, DeviceType, Location, Vendor
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


class MasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name", "description", "is_deleted", "deleted_at", "created_at", "updated_at"]
        read_only_fields = ["id", "is_deleted", "deleted_at", "created_at", "updated_at"]

    def validate_code(self, value):
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError("Code is required.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_description(self, value):
        return value.strip()


class AssetTypeSerializer(MasterDataSerializer):
    class Meta(MasterDataSerializer.Meta):
        model = AssetType


class VendorSerializer(MasterDataSerializer):
    class Meta(MasterDataSerializer.Meta):
        model = Vendor


class DeviceTypeSerializer(MasterDataSerializer):
    class Meta(MasterDataSerializer.Meta):
        model = DeviceType


class LocationSerializer(MasterDataSerializer):
    class Meta(MasterDataSerializer.Meta):
        model = Location


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
        queryset=Site.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source="location",
        queryset=Location.objects.active(),
        required=False,
        allow_null=True,
        write_only=True,
    )

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

    def validate(self, attrs):
        warranty_starts_on = attrs.get("warranty_starts_on", getattr(self.instance, "warranty_starts_on", None))
        warranty_expires_on = attrs.get("warranty_expires_on", getattr(self.instance, "warranty_expires_on", None))
        purchase_date = attrs.get("purchase_date", getattr(self.instance, "purchase_date", None))

        errors = {}

        if warranty_starts_on and warranty_expires_on and warranty_expires_on < warranty_starts_on:
            errors["warranty_expires_on"] = "Warranty expiry cannot be before warranty start."

        if purchase_date and purchase_date > date.today():
            errors["purchase_date"] = "Purchase date cannot be in the future."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
