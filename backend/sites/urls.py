from django.urls import path

from sites.views import SiteDetailView, SiteListCreateView


urlpatterns = [
    path("sites", SiteListCreateView.as_view(), name="site-list"),
    path("sites/<int:site_id>", SiteDetailView.as_view(), name="site-detail"),
]
