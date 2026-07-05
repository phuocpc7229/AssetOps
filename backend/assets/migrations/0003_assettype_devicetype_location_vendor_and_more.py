import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone


def build_code(value, fallback):
    value = (value or "").strip()
    if not value:
        return fallback

    code = "".join(character if character.isalnum() else "_" for character in value.upper())
    code = "_".join(part for part in code.split("_") if part)
    return (code or fallback)[:40]


def get_or_create_master(model, value, fallback_code, fallback_name):
    value = (value or "").strip()
    code = build_code(value, fallback_code)
    name = value or fallback_name
    base_code = code
    suffix = 2

    while True:
        item = model.objects.filter(code=code).first()
        if item is None:
            return model.objects.create(code=code, name=name)
        if item.name == name:
            return item

        suffix_text = f"_{suffix}"
        code = f"{base_code[:40 - len(suffix_text)]}{suffix_text}"
        suffix += 1


def migrate_asset_master_data(apps, schema_editor):
    Asset = apps.get_model("assets", "Asset")
    AssetType = apps.get_model("assets", "AssetType")
    Vendor = apps.get_model("assets", "Vendor")
    Location = apps.get_model("assets", "Location")

    for asset in Asset.objects.all().iterator():
        asset_type = get_or_create_master(
            AssetType,
            getattr(asset, "asset_type_legacy", ""),
            "UNKNOWN",
            "Unknown",
        )
        asset.asset_type = asset_type

        vendor_value = getattr(asset, "vendor_legacy", "")
        if vendor_value.strip():
            asset.vendor = get_or_create_master(Vendor, vendor_value, "UNKNOWN_VENDOR", vendor_value)

        location_value = getattr(asset, "location_legacy", "")
        if location_value.strip():
            asset.location = get_or_create_master(Location, location_value, "UNKNOWN_LOCATION", location_value)

        asset.updated_at = timezone.now()
        asset.save(update_fields=["asset_type", "vendor", "location", "updated_at"])


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_alter_asset_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'asset_types',
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'device_types',
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'locations',
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'vendors',
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.RemoveIndex(
            model_name='asset',
            name='assets_asset_type_idx',
        ),
        migrations.RemoveIndex(
            model_name='asset',
            name='assets_vendor_idx',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='asset_type',
            new_name='asset_type_legacy',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='vendor',
            new_name='vendor_legacy',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='location',
            new_name='location_legacy',
        ),
        migrations.AddIndex(
            model_name='assettype',
            index=models.Index(fields=['code'], name='asset_types_code_idx'),
        ),
        migrations.AddIndex(
            model_name='assettype',
            index=models.Index(fields=['name'], name='asset_types_name_idx'),
        ),
        migrations.AddIndex(
            model_name='assettype',
            index=models.Index(fields=['is_deleted'], name='asset_types_deleted_idx'),
        ),
        migrations.AddField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='assets.assettype'),
        ),
        migrations.AddIndex(
            model_name='devicetype',
            index=models.Index(fields=['code'], name='device_types_code_idx'),
        ),
        migrations.AddIndex(
            model_name='devicetype',
            index=models.Index(fields=['name'], name='device_types_name_idx'),
        ),
        migrations.AddIndex(
            model_name='devicetype',
            index=models.Index(fields=['is_deleted'], name='device_types_deleted_idx'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['code'], name='locations_code_idx'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['name'], name='locations_name_idx'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['is_deleted'], name='locations_deleted_idx'),
        ),
        migrations.AddField(
            model_name='asset',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assets', to='assets.location'),
        ),
        migrations.AddIndex(
            model_name='vendor',
            index=models.Index(fields=['code'], name='vendors_code_idx'),
        ),
        migrations.AddIndex(
            model_name='vendor',
            index=models.Index(fields=['name'], name='vendors_name_idx'),
        ),
        migrations.AddIndex(
            model_name='vendor',
            index=models.Index(fields=['is_deleted'], name='vendors_deleted_idx'),
        ),
        migrations.AddField(
            model_name='asset',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assets', to='assets.vendor'),
        ),
        migrations.RunPython(migrate_asset_master_data, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='assets.assettype'),
        ),
        migrations.RemoveField(
            model_name='asset',
            name='asset_type_legacy',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='vendor_legacy',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='location_legacy',
        ),
    ]
