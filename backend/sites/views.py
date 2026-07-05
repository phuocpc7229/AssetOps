from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sites.models import Site
from sites.serializers import SiteSerializer


ORDERING_FIELDS = {"code", "name", "created_at", "updated_at"}


def should_include_deleted(value: str | None) -> bool:
    return value is not None and value.lower() in {"1", "true", "yes"}


class SiteListCreateView(APIView):
    def get(self, request):
        queryset = Site.objects.all()
        if not should_include_deleted(request.query_params.get("include_deleted")):
            queryset = queryset.active()

        search = request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | Q(name__icontains=search) | Q(address__icontains=search)
            )

        queryset = queryset.order_by(*self.get_ordering(request))
        page_size = self.get_page_size(request)
        paginator = Paginator(queryset, page_size)
        page_number = self.get_page_number(request)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages or 1)

        serializer = SiteSerializer(page.object_list, many=True)
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
        serializer = SiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        site = serializer.save()
        return Response(SiteSerializer(site).data, status=status.HTTP_201_CREATED)

    def get_ordering(self, request):
        requested_ordering = request.query_params.get("ordering", "code")
        ordering = []

        for field in requested_ordering.split(","):
            field = field.strip()
            field_name = field.removeprefix("-")
            if field_name in ORDERING_FIELDS:
                ordering.append(field)

        return ordering or ["code"]

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


class SiteDetailView(APIView):
    def get_site(self, site_id):
        return Site.objects.active().filter(pk=site_id).first()

    def get(self, request, site_id):
        site = self.get_site(site_id)
        if site is None:
            return Response({"detail": "Site not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(SiteSerializer(site).data)

    def patch(self, request, site_id):
        site = self.get_site(site_id)
        if site is None:
            return Response({"detail": "Site not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SiteSerializer(site, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        site = serializer.save()
        return Response(SiteSerializer(site).data)

    def delete(self, request, site_id):
        site = self.get_site(site_id)
        if site is None:
            return Response({"detail": "Site not found."}, status=status.HTTP_404_NOT_FOUND)

        site.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
