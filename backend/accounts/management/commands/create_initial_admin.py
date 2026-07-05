import os

from django.core.management.base import BaseCommand, CommandError

from accounts.models import AdminUser
from accounts.security import hash_password


class Command(BaseCommand):
    help = "Create or update the initial administrator from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("ASSETOPS_ADMIN_USERNAME")
        password = os.getenv("ASSETOPS_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError("ASSETOPS_ADMIN_USERNAME and ASSETOPS_ADMIN_PASSWORD are required.")

        user, created = AdminUser.objects.get_or_create(
            username=username,
            defaults={
                "password_hash": hash_password(password),
                "is_active": True,
                "is_superuser": True,
            },
        )

        if not created:
            changed_fields = []
            if not user.is_active:
                user.is_active = True
                changed_fields.append("is_active")
            if not user.is_superuser:
                user.is_superuser = True
                changed_fields.append("is_superuser")
            if os.getenv("ASSETOPS_ADMIN_UPDATE_PASSWORD", "false").lower() in {"1", "true", "yes"}:
                user.password_hash = hash_password(password)
                changed_fields.append("password_hash")
            if changed_fields:
                user.save(update_fields=changed_fields)

        action = "created" if created else "already exists"
        self.stdout.write(self.style.SUCCESS(f"Initial administrator {action}: {username}"))
