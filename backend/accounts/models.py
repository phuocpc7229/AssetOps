from django.db import models


class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admin_users"
        indexes = [
            models.Index(fields=["username"], name="admin_users_username_idx"),
        ]

    @property
    def is_authenticated(self) -> bool:
        return True

    def __str__(self) -> str:
        return self.username


class AccessToken(models.Model):
    user = models.ForeignKey(AdminUser, related_name="access_tokens", on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "access_tokens"
        indexes = [
            models.Index(fields=["token_hash"], name="access_tokens_hash_idx"),
        ]
