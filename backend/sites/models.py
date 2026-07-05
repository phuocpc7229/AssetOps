from django.db import models
from django.utils import timezone


class SiteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)


class Site(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    address = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SiteQuerySet.as_manager()

    class Meta:
        db_table = "sites"
        indexes = [
            models.Index(fields=["code"], name="sites_code_idx"),
            models.Index(fields=["name"], name="sites_name_idx"),
            models.Index(fields=["is_deleted"], name="sites_deleted_idx"),
        ]
        ordering = ["code"]

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
