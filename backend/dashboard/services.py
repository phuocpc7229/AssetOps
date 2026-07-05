from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone

from assets.models import Asset, AssetType, DeviceType, Location, Vendor
from sites.models import Site


CHART_COLORS = ["#0A84FF", "#7357FF", "#11C6C8", "#00D48A", "#FF951A", "#8B4DFF"]


def build_dashboard_metrics() -> dict:
    today = timezone.localdate()
    expiring_until = today + timedelta(days=30)
    six_months_out = today + timedelta(days=180)

    total_assets = Asset.objects.count()
    non_archived_queryset = Asset.objects.exclude(status=Asset.Status.ARCHIVED)
    non_archived_total = non_archived_queryset.count()
    active_assets = Asset.objects.filter(status=Asset.Status.ACTIVE).count()
    maintenance_assets = Asset.objects.filter(status=Asset.Status.IN_MAINTENANCE).count()
    archived_assets = Asset.objects.filter(status=Asset.Status.ARCHIVED).count()
    expiring_warranty = non_archived_queryset.filter(
        warranty_expires_on__gte=today,
        warranty_expires_on__lte=expiring_until,
    ).count()
    online_assets = get_online_assets_queryset().count()

    return {
        "generated_at": timezone.now().isoformat(),
        "kpis": [
            build_kpi(
                key="total_assets",
                label="Total Assets",
                value=total_assets,
                helper="All registered assets",
                percent=None,
                tone="blue",
                trend=build_trend(Asset.objects.all(), "created_at"),
            ),
            build_kpi(
                key="active_assets",
                label="Active Assets",
                value=active_assets,
                helper=f"{format_percent(active_assets, total_assets)} of total",
                percent=calculate_percent(active_assets, total_assets),
                tone="green",
                trend=build_trend(Asset.objects.filter(status=Asset.Status.ACTIVE), "updated_at"),
            ),
            build_kpi(
                key="maintenance_assets",
                label="In Maintenance",
                value=maintenance_assets,
                helper=f"{format_percent(maintenance_assets, total_assets)} of total",
                percent=calculate_percent(maintenance_assets, total_assets),
                tone="orange",
                trend=build_trend(Asset.objects.filter(status=Asset.Status.IN_MAINTENANCE), "updated_at"),
            ),
            build_kpi(
                key="expiring_warranty",
                label="Expiring Warranty",
                value=expiring_warranty,
                helper=f"{format_percent(expiring_warranty, non_archived_total)} of active inventory",
                percent=calculate_percent(expiring_warranty, non_archived_total),
                tone="orange",
                trend=build_trend(
                    non_archived_queryset.filter(
                        warranty_expires_on__gte=today,
                        warranty_expires_on__lte=expiring_until,
                    ),
                    "updated_at",
                ),
            ),
            build_kpi(
                key="online_assets",
                label="Online Assets",
                value=online_assets,
                helper=f"{format_percent(online_assets, non_archived_total)} with assigned IPs",
                percent=calculate_percent(online_assets, non_archived_total),
                tone="blue",
                trend=build_trend(get_online_assets_queryset(), "updated_at"),
            ),
        ],
        "charts": {
            "assets_by_type": build_assets_by_type_chart(non_archived_queryset),
            "warranty_status": build_warranty_status_chart(non_archived_queryset, today, expiring_until, six_months_out),
        },
        "quick_action_badges": {
            "maintenance_assets": maintenance_assets,
            "archived_assets": archived_assets,
            "expiring_warranty": expiring_warranty,
        },
    }


def build_recent_assets(limit: int = 8) -> list[dict]:
    assets = (
        Asset.objects.select_related("asset_type", "vendor", "site", "location")
        .prefetch_related("ip_addresses")
        .annotate(ip_count_value=Count("ip_addresses", distinct=True))
        .order_by("-updated_at", "-id")[:limit]
    )

    return [serialize_dashboard_asset(asset) for asset in assets]


def build_recent_activity(limit: int = 8) -> list[dict]:
    candidates = []
    candidates.extend(build_asset_activity(limit))
    candidates.extend(build_site_activity(limit))
    candidates.extend(build_master_data_activity(limit))
    candidates.sort(key=lambda item: item["occurred_at"], reverse=True)
    return candidates[:limit]


def get_online_assets_queryset():
    return Asset.objects.exclude(status=Asset.Status.ARCHIVED).filter(ip_address__isnull=False)


def build_kpi(key: str, label: str, value: int, helper: str, percent: float | None, tone: str, trend: list[dict]) -> dict:
    return {
        "key": key,
        "label": label,
        "value": value,
        "helper": helper,
        "percent": percent,
        "tone": tone,
        "trend": trend,
    }


def build_trend(queryset, date_field: str, days: int = 14) -> list[dict]:
    today = timezone.localdate()
    start_date = today - timedelta(days=days - 1)
    grouped_rows = (
        queryset.filter(**{f"{date_field}__date__gte": start_date})
        .annotate(day=TruncDate(date_field))
        .values("day")
        .annotate(value=Count("id"))
    )
    values_by_day = {row["day"]: row["value"] for row in grouped_rows}

    return [
        {
            "date": (start_date + timedelta(days=index)).isoformat(),
            "value": values_by_day.get(start_date + timedelta(days=index), 0),
        }
        for index in range(days)
    ]


def build_assets_by_type_chart(queryset) -> dict:
    total = queryset.count()
    rows = list(
        queryset.values("asset_type_id", "asset_type__code", "asset_type__name")
        .annotate(value=Count("id"))
        .order_by("-value", "asset_type__code")
    )
    visible_rows = rows[:5]
    hidden_total = sum(row["value"] for row in rows[5:])
    segments = []

    for index, row in enumerate(visible_rows):
        segments.append(
            {
                "key": row["asset_type__code"],
                "label": row["asset_type__name"],
                "value": row["value"],
                "percent": calculate_percent(row["value"], total),
                "color": CHART_COLORS[index % len(CHART_COLORS)],
            }
        )

    if hidden_total:
        segments.append(
            {
                "key": "other",
                "label": "Other",
                "value": hidden_total,
                "percent": calculate_percent(hidden_total, total),
                "color": CHART_COLORS[-1],
            }
        )

    return {"total": total, "segments": segments}


def build_warranty_status_chart(queryset, today, expiring_until, six_months_out) -> dict:
    total = queryset.count()
    buckets = [
        (
            "valid_gt_6_months",
            "Valid > 6 months",
            queryset.filter(warranty_expires_on__gt=six_months_out).count(),
            "#00D48A",
        ),
        (
            "valid_1_6_months",
            "Valid 1-6 months",
            queryset.filter(warranty_expires_on__gt=expiring_until, warranty_expires_on__lte=six_months_out).count(),
            "#0A84FF",
        ),
        (
            "expiring_lt_30_days",
            "Expiring < 30 days",
            queryset.filter(warranty_expires_on__gte=today, warranty_expires_on__lte=expiring_until).count(),
            "#FF951A",
        ),
        ("expired", "Expired", queryset.filter(warranty_expires_on__lt=today).count(), "#FF4D5E"),
        ("unknown", "Unknown", queryset.filter(warranty_expires_on__isnull=True).count(), "#7357FF"),
    ]

    return {
        "total": total,
        "segments": [
            {
                "key": key,
                "label": label,
                "value": value,
                "percent": calculate_percent(value, total),
                "color": color,
            }
            for key, label, value, color in buckets
            if value > 0
        ],
    }


def serialize_dashboard_asset(asset: Asset) -> dict:
    return {
        "id": asset.id,
        "asset_tag": asset.asset_tag,
        "name": asset.name,
        "primary_ip": asset.ip_address,
        "ip_count": asset.ip_count_value,
        "asset_type": serialize_master_record(asset.asset_type),
        "vendor": serialize_master_record(asset.vendor),
        "site": serialize_site(asset.site),
        "status": asset.status,
        "criticality": asset.criticality,
        "warranty_expires_on": asset.warranty_expires_on.isoformat() if asset.warranty_expires_on else None,
        "warranty_state": get_warranty_state(asset),
        "updated_at": asset.updated_at.isoformat(),
    }


def serialize_master_record(record) -> dict | None:
    if record is None:
        return None

    return {"id": record.id, "code": record.code, "name": record.name}


def serialize_site(site: Site | None) -> dict | None:
    if site is None:
        return None

    return {"id": site.id, "code": site.code, "name": site.name}


def get_warranty_state(asset: Asset) -> str:
    if asset.warranty_expires_on is None:
        return "unknown"

    today = timezone.localdate()
    if asset.warranty_expires_on < today:
        return "expired"
    if asset.warranty_expires_on <= today + timedelta(days=30):
        return "expiring"
    return "valid"


def build_asset_activity(limit: int) -> list[dict]:
    assets = Asset.objects.order_by("-updated_at", "-id")[:limit]
    return [
        {
            "id": f"asset-{asset.id}",
            "occurred_at": asset.updated_at.isoformat(),
            "entity_type": "asset",
            "action": get_record_action(asset, archived=asset.status == Asset.Status.ARCHIVED),
            "title": asset.asset_tag,
            "metadata": asset.name,
            "severity": get_asset_activity_severity(asset),
            "route": f"/dashboard/assets/{asset.id}/edit",
        }
        for asset in assets
    ]


def build_site_activity(limit: int) -> list[dict]:
    sites = Site.objects.order_by("-updated_at", "-id")[:limit]
    return [
        {
            "id": f"site-{site.id}",
            "occurred_at": site.updated_at.isoformat(),
            "entity_type": "site",
            "action": get_record_action(site, archived=site.is_deleted),
            "title": site.code,
            "metadata": site.name,
            "severity": "warning" if site.is_deleted else "info",
            "route": "/dashboard/sites",
        }
        for site in sites
    ]


def build_master_data_activity(limit: int) -> list[dict]:
    records = []
    models = [
        (AssetType, "asset-types", "Asset Type"),
        (Vendor, "vendors", "Vendor"),
        (DeviceType, "device-types", "Device Type"),
        (Location, "locations", "Location"),
    ]

    for model, route_kind, label in models:
        for record in model.objects.order_by("-updated_at", "-id")[:limit]:
            records.append(
                {
                    "id": f"{route_kind}-{record.id}",
                    "occurred_at": record.updated_at.isoformat(),
                    "entity_type": "master_data",
                    "action": get_record_action(record, archived=record.is_deleted),
                    "title": record.code,
                    "metadata": f"{label}: {record.name}",
                    "severity": "warning" if record.is_deleted else "info",
                    "route": f"/dashboard/master-data/{route_kind}",
                }
            )

    return records


def get_record_action(record, archived: bool = False) -> str:
    if archived:
        return "archived"

    if abs((record.updated_at - record.created_at).total_seconds()) <= 1:
        return "created"

    return "updated"


def get_asset_activity_severity(asset: Asset) -> str:
    if asset.status == Asset.Status.ARCHIVED:
        return "warning"
    if asset.criticality == Asset.Criticality.CRITICAL:
        return "danger"
    if asset.status == Asset.Status.ACTIVE:
        return "success"
    return "info"


def calculate_percent(value: int, total: int) -> float:
    if total <= 0:
        return 0

    return round((value / total) * 100, 1)


def format_percent(value: int, total: int) -> str:
    return f"{calculate_percent(value, total)}%"
