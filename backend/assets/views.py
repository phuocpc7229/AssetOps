import platform
import re
import subprocess
import time

from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assets.models import Asset, AssetType, DeviceType, Location, Vendor
from assets.serializers import (
    AssetSerializer,
    AssetTypeSerializer,
    DeviceTypeSerializer,
    LocationSerializer,
    VendorSerializer,
)


LIST_FILTERS = ["status", "criticality", "asset_type", "vendor"]
ORDERING_FIELDS = {
    "asset_tag",
    "name",
    "hostname",
    "asset_type__code",
    "asset_type__name",
    "vendor__code",
    "vendor__name",
    "site",
    "status",
    "criticality",
    "warranty_expires_on",
    "purchase_date",
    "created_at",
    "updated_at",
}
MASTER_DATA_ORDERING_FIELDS = {"code", "name", "created_at", "updated_at"}


def should_include_archived(value: str | None) -> bool:
    return value is not None and value.lower() in {"1", "true", "yes"}


class AssetListCreateView(APIView):
    def get(self, request):
        queryset = Asset.objects.select_related("asset_type", "vendor", "site", "location").all()

        if not should_include_archived(request.query_params.get("include_archived")):
            queryset = queryset.exclude(status=Asset.Status.ARCHIVED)

        search = request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(asset_tag__icontains=search)
                | Q(name__icontains=search)
                | Q(hostname__icontains=search)
                | Q(serial_number__icontains=search)
                | Q(ip_address__icontains=search)
                | Q(asset_type__code__icontains=search)
                | Q(asset_type__name__icontains=search)
                | Q(vendor__code__icontains=search)
                | Q(vendor__name__icontains=search)
                | Q(location__code__icontains=search)
                | Q(location__name__icontains=search)
            )

        for filter_name in ["status", "criticality"]:
            value = request.query_params.get(filter_name, "").strip()
            if value:
                queryset = queryset.filter(**{filter_name: value})

        queryset = self.filter_master_data(queryset, request, "asset_type")
        queryset = self.filter_master_data(queryset, request, "vendor")
        queryset = self.filter_master_data(queryset, request, "location")

        site = request.query_params.get("site", "").strip()
        if site:
            if site.isdigit():
                queryset = queryset.filter(site_id=int(site))
            else:
                queryset = queryset.filter(Q(site__code__iexact=site) | Q(site__name__iexact=site))

        queryset = queryset.order_by(*self.get_ordering(request))
        page_size = self.get_page_size(request)
        paginator = Paginator(queryset, page_size)
        page_number = self.get_page_number(request)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages or 1)

        serializer = AssetSerializer(page.object_list, many=True)
        return Response(
            {
                "count": paginator.count,
                "page": page.number,
                "page_size": page_size,
                "total_pages": paginator.num_pages,
                "results": serializer.data,
            }
        )

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset = serializer.save(created_by=request.user, updated_by=request.user)
        return Response(AssetSerializer(asset).data, status=status.HTTP_201_CREATED)

    def get_ordering(self, request):
        requested_ordering = request.query_params.get("ordering", "asset_tag")
        ordering = []

        for field in requested_ordering.split(","):
            field = field.strip()
            field_name = field.removeprefix("-")
            if field_name in ORDERING_FIELDS:
                ordering.append(field)

        return ordering or ["asset_tag"]

    def filter_master_data(self, queryset, request, field_name: str):
        value = request.query_params.get(field_name, "").strip()
        if not value:
            return queryset

        if value.isdigit():
            return queryset.filter(**{f"{field_name}_id": int(value)})

        return queryset.filter(
            Q(**{f"{field_name}__code__iexact": value}) | Q(**{f"{field_name}__name__iexact": value})
        )

    def get_page_number(self, request) -> int:
        try:
            return max(int(request.query_params.get("page", 1)), 1)
        except ValueError:
            return 1

    def get_page_size(self, request) -> int:
        try:
            page_size = int(request.query_params.get("page_size", 10))
        except ValueError:
            return 10

        return min(max(page_size, 1), 100)


class AssetDetailView(APIView):
    def get_asset(self, asset_id):
        return Asset.objects.select_related("asset_type", "vendor", "site", "location").filter(pk=asset_id).first()

    def get(self, request, asset_id):
        asset = self.get_asset(asset_id)
        if asset is None:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(AssetSerializer(asset).data)

    def patch(self, request, asset_id):
        asset = self.get_asset(asset_id)
        if asset is None:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssetSerializer(asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        asset = serializer.save(updated_by=request.user)
        return Response(AssetSerializer(asset).data)

    def delete(self, request, asset_id):
        asset = self.get_asset(asset_id)
        if asset is None:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)

        asset.status = Asset.Status.ARCHIVED
        asset.updated_by = request.user
        asset.save(update_fields=["status", "updated_by", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssetPingView(APIView):
    def post(self, request, asset_id):
        asset = Asset.objects.filter(pk=asset_id).first()
        if asset is None:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)

        if not asset.ip_address:
            return Response(
                {"detail": "Ping test requires an asset IP address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = ping_ip_address(asset.ip_address)
        return Response(result)


class MasterDataListCreateView(APIView):
    model = None
    serializer_class = None
    default_ordering = "code"

    def get(self, request):
        queryset = self.model.objects.all()

        if not should_include_archived(request.query_params.get("include_deleted")):
            queryset = queryset.active()

        search = request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | Q(name__icontains=search) | Q(description__icontains=search)
            )

        queryset = queryset.order_by(*self.get_ordering(request))
        page_size = self.get_page_size(request)
        paginator = Paginator(queryset, page_size)
        page_number = self.get_page_number(request)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages or 1)

        serializer = self.serializer_class(page.object_list, many=True)
        return Response(
            {
                "count": paginator.count,
                "page": page.number,
                "page_size": page_size,
                "total_pages": paginator.num_pages,
                "results": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(self.serializer_class(item).data, status=status.HTTP_201_CREATED)

    def get_ordering(self, request):
        requested_ordering = request.query_params.get("ordering", self.default_ordering)
        ordering = []

        for field in requested_ordering.split(","):
            field = field.strip()
            field_name = field.removeprefix("-")
            if field_name in MASTER_DATA_ORDERING_FIELDS:
                ordering.append(field)

        return ordering or [self.default_ordering]

    def get_page_number(self, request) -> int:
        try:
            return max(int(request.query_params.get("page", 1)), 1)
        except ValueError:
            return 1

    def get_page_size(self, request) -> int:
        try:
            page_size = int(request.query_params.get("page_size", 50))
        except ValueError:
            return 50

        return min(max(page_size, 1), 100)


class MasterDataDetailView(APIView):
    model = None
    serializer_class = None
    not_found_message = "Master data record not found."

    def get_item(self, item_id):
        return self.model.objects.filter(pk=item_id).first()

    def get(self, request, item_id):
        item = self.get_item(item_id)
        if item is None:
            return Response({"detail": self.not_found_message}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.serializer_class(item).data)

    def patch(self, request, item_id):
        item = self.get_item(item_id)
        if item is None:
            return Response({"detail": self.not_found_message}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(self.serializer_class(item).data)

    def delete(self, request, item_id):
        item = self.get_item(item_id)
        if item is None:
            return Response({"detail": self.not_found_message}, status=status.HTTP_404_NOT_FOUND)

        item.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssetTypeListCreateView(MasterDataListCreateView):
    model = AssetType
    serializer_class = AssetTypeSerializer


class AssetTypeDetailView(MasterDataDetailView):
    model = AssetType
    serializer_class = AssetTypeSerializer
    not_found_message = "Asset type not found."


class VendorListCreateView(MasterDataListCreateView):
    model = Vendor
    serializer_class = VendorSerializer


class VendorDetailView(MasterDataDetailView):
    model = Vendor
    serializer_class = VendorSerializer
    not_found_message = "Vendor not found."


class DeviceTypeListCreateView(MasterDataListCreateView):
    model = DeviceType
    serializer_class = DeviceTypeSerializer


class DeviceTypeDetailView(MasterDataDetailView):
    model = DeviceType
    serializer_class = DeviceTypeSerializer
    not_found_message = "Device type not found."


class LocationListCreateView(MasterDataListCreateView):
    model = Location
    serializer_class = LocationSerializer


class LocationDetailView(MasterDataDetailView):
    model = Location
    serializer_class = LocationSerializer
    not_found_message = "Location not found."


def ping_ip_address(ip_address: str) -> dict:
    command = build_ping_command(ip_address)
    started_at = time.perf_counter()

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "ip_address": ip_address,
            "latency_ms": None,
            "message": "Ping timed out.",
        }
    except OSError:
        return {
            "success": False,
            "ip_address": ip_address,
            "latency_ms": None,
            "message": "Ping command is not available.",
        }

    output = f"{completed.stdout}\n{completed.stderr}"
    latency_ms = parse_latency_ms(output)
    if latency_ms is None and completed.returncode == 0:
        latency_ms = round((time.perf_counter() - started_at) * 1000, 2)

    success = completed.returncode == 0
    return {
        "success": success,
        "ip_address": ip_address,
        "latency_ms": latency_ms,
        "message": "Ping successful." if success else "Ping failed.",
    }


def build_ping_command(ip_address: str) -> list[str]:
    if platform.system().lower() == "windows":
        return ["ping", "-n", "1", "-w", "1000", ip_address]

    return ["ping", "-c", "1", "-W", "1", ip_address]


def parse_latency_ms(output: str) -> float | None:
    match = re.search(r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms", output, re.IGNORECASE)
    if match is None:
        return None

    return float(match.group(1))
