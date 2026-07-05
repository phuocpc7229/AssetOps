from django.core.management.base import BaseCommand

from assets.models import AssetType, DeviceType, Location, Vendor


DEFAULT_ASSET_TYPES = [
    ("SERVER", "Server"),
    ("SWITCH", "Network Switch"),
    ("FIREWALL", "Firewall"),
    ("ROUTER", "Router"),
    ("LAPTOP", "Laptop"),
    ("DESKTOP", "Desktop"),
    ("PRINTER", "Printer"),
    ("AP", "Access Point"),
    ("STORAGE", "Storage"),
    ("UPS", "UPS"),
    ("CAMERA", "CCTV Camera"),
]

DEFAULT_VENDORS = [
    ("CISCO", "Cisco"),
    ("HUAWEI", "Huawei"),
    ("DELL", "Dell"),
    ("HPE", "HPE"),
    ("LENOVO", "Lenovo"),
    ("FORTINET", "Fortinet"),
    ("ARUBA", "Aruba"),
    ("UBIQUITI", "Ubiquiti"),
    ("SYNOLOGY", "Synology"),
    ("QNAP", "QNAP"),
    ("APC", "APC"),
]

DEFAULT_DEVICE_TYPES = [
    ("CORE-SW", "Core Switch"),
    ("ACCESS-SW", "Access Switch"),
    ("DIST-SW", "Distribution Switch"),
    ("RACK-SRV", "Rack Server"),
    ("TOWER-SRV", "Tower Server"),
    ("VIRTUAL-MACHINE", "Virtual Machine"),
    ("WIFI-AP", "Wireless Access Point"),
    ("EDGE-FW", "Edge Firewall"),
]

DEFAULT_LOCATIONS = [
    ("SRV-ROOM", "Server Room"),
    ("MDF", "Main Distribution Frame"),
    ("IDF", "Intermediate Distribution Frame"),
    ("RACK-A01", "Rack A01"),
    ("RACK-B01", "Rack B01"),
    ("IT-OFFICE", "IT Office"),
    ("STORAGE", "Storage Room"),
    ("WAREHOUSE", "Warehouse"),
    ("FLOOR-01", "Floor 01"),
    ("FLOOR-02", "Floor 02"),
    ("FLOOR-03", "Floor 03"),
]


class Command(BaseCommand):
    help = "Seed default AssetOps master data records."

    def handle(self, *args, **options):
        created_count = 0
        created_count += self.seed_records(AssetType, DEFAULT_ASSET_TYPES)
        created_count += self.seed_records(Vendor, DEFAULT_VENDORS)
        created_count += self.seed_records(DeviceType, DEFAULT_DEVICE_TYPES)
        created_count += self.seed_records(Location, DEFAULT_LOCATIONS)

        self.stdout.write(self.style.SUCCESS(f"Seeded master data. Created {created_count} records."))

    def seed_records(self, model, records):
        created_count = 0

        for code, name in records:
            _, created = model.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": "",
                },
            )
            if created:
                created_count += 1

        return created_count
