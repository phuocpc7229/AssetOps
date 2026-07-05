from django.db import models
from django.db.models import Q
from django.utils import timezone


class MasterDataQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)


class MasterDataModel(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MasterDataQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ["code"]

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class AssetType(MasterDataModel):
    class Meta(MasterDataModel.Meta):
        db_table = "asset_types"
        indexes = [
            models.Index(fields=["code"], name="asset_types_code_idx"),
            models.Index(fields=["name"], name="asset_types_name_idx"),
            models.Index(fields=["is_deleted"], name="asset_types_deleted_idx"),
        ]


class Vendor(MasterDataModel):
    class Meta(MasterDataModel.Meta):
        db_table = "vendors"
        indexes = [
            models.Index(fields=["code"], name="vendors_code_idx"),
            models.Index(fields=["name"], name="vendors_name_idx"),
            models.Index(fields=["is_deleted"], name="vendors_deleted_idx"),
        ]


class DeviceType(MasterDataModel):
    class Meta(MasterDataModel.Meta):
        db_table = "device_types"
        indexes = [
            models.Index(fields=["code"], name="device_types_code_idx"),
            models.Index(fields=["name"], name="device_types_name_idx"),
            models.Index(fields=["is_deleted"], name="device_types_deleted_idx"),
        ]


class Location(MasterDataModel):
    class Meta(MasterDataModel.Meta):
        db_table = "locations"
        indexes = [
            models.Index(fields=["code"], name="locations_code_idx"),
            models.Index(fields=["name"], name="locations_name_idx"),
            models.Index(fields=["is_deleted"], name="locations_deleted_idx"),
        ]


class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        IN_MAINTENANCE = "in_maintenance", "In Maintenance"
        ARCHIVED = "archived", "Archived"

    class Criticality(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    asset_tag = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=180)
    hostname = models.CharField(max_length=180, blank=True)
    asset_type = models.ForeignKey("assets.AssetType", related_name="assets", on_delete=models.PROTECT)
    vendor = models.ForeignKey(
        "assets.Vendor",
        related_name="assets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    model = models.CharField(max_length=120, blank=True)
    serial_number = models.CharField(max_length=120, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=17, blank=True)
    site = models.ForeignKey(
        "sites.Site",
        related_name="assets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    location = models.ForeignKey(
        "assets.Location",
        related_name="assets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.ACTIVE)
    criticality = models.CharField(max_length=32, choices=Criticality.choices, default=Criticality.MEDIUM)
    warranty_starts_on = models.DateField(null=True, blank=True)
    warranty_expires_on = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.AdminUser",
        related_name="created_assets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        "accounts.AdminUser",
        related_name="updated_assets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "assets"
        constraints = [
            models.UniqueConstraint(
                fields=["serial_number"],
                condition=~Q(serial_number=""),
                name="assets_serial_number_unique_when_present",
            ),
        ]
        indexes = [
            models.Index(fields=["asset_tag"], name="assets_asset_tag_idx"),
            models.Index(fields=["status"], name="assets_status_idx"),
            models.Index(fields=["criticality"], name="assets_criticality_idx"),
            models.Index(fields=["site"], name="assets_site_idx"),
            models.Index(fields=["warranty_expires_on"], name="assets_warranty_exp_idx"),
        ]
        ordering = ["asset_tag"]

    def __str__(self) -> str:
        return f"{self.asset_tag} - {self.name}"
