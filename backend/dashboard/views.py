from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services import build_dashboard_metrics, build_recent_activity, build_recent_assets


class DashboardMetricsView(APIView):
    def get(self, request):
        return Response(build_dashboard_metrics())


class DashboardRecentAssetsView(APIView):
    def get(self, request):
        return Response({"results": build_recent_assets(get_limit(request))})


class DashboardRecentActivityView(APIView):
    def get(self, request):
        return Response(
            {
                "source": "temporary_inferred",
                "note": "Recent activity is inferred from existing records until an AuditEvent table exists.",
                "results": build_recent_activity(get_limit(request)),
            }
        )


def get_limit(request, default: int = 8, maximum: int = 20) -> int:
    try:
        requested_limit = int(request.query_params.get("limit", default))
    except ValueError:
        return default

    return min(max(requested_limit, 1), maximum)
