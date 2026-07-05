from django.urls import path

from dashboard.views import DashboardMetricsView, DashboardRecentActivityView, DashboardRecentAssetsView


urlpatterns = [
    path("dashboard/metrics", DashboardMetricsView.as_view(), name="dashboard-metrics"),
    path("dashboard/recent-assets", DashboardRecentAssetsView.as_view(), name="dashboard-recent-assets"),
    path("dashboard/recent-activity", DashboardRecentActivityView.as_view(), name="dashboard-recent-activity"),
]
