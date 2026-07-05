from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdminUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("username", models.CharField(max_length=150, unique=True)),
                ("password_hash", models.CharField(max_length=256)),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "admin_users",
            },
        ),
        migrations.CreateModel(
            name="AccessToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token_hash", models.CharField(max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_used_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="access_tokens",
                        to="accounts.adminuser",
                    ),
                ),
            ],
            options={
                "db_table": "access_tokens",
            },
        ),
        migrations.AddIndex(
            model_name="adminuser",
            index=models.Index(fields=["username"], name="admin_users_username_idx"),
        ),
        migrations.AddIndex(
            model_name="accesstoken",
            index=models.Index(fields=["token_hash"], name="access_tokens_hash_idx"),
        ),
    ]
