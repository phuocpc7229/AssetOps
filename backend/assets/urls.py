from django.urls import path

from assets.views import (
    AssetDetailView,
    AssetListCreateView,
    AssetPingView,
    AssetTypeDetailView,
    AssetTypeListCreateView,
    DeviceTypeDetailView,
    DeviceTypeListCreateView,
    LocationDetailView,
    LocationListCreateView,
    VendorDetailView,
    VendorListCreateView,
)


urlpatterns = [
    path("asset-types", AssetTypeListCreateView.as_view(), name="asset-type-list"),
    path("asset-types/<int:item_id>", AssetTypeDetailView.as_view(), name="asset-type-detail"),
    path("vendors", VendorListCreateView.as_view(), name="vendor-list"),
    path("vendors/<int:item_id>", VendorDetailView.as_view(), name="vendor-detail"),
    path("device-types", DeviceTypeListCreateView.as_view(), name="device-type-list"),
    path("device-types/<int:item_id>", DeviceTypeDetailView.as_view(), name="device-type-detail"),
    path("locations", LocationListCreateView.as_view(), name="location-list"),
    path("locations/<int:item_id>", LocationDetailView.as_view(), name="location-detail"),
    path("assets", AssetListCreateView.as_view(), name="asset-list"),
    path("assets/<int:asset_id>", AssetDetailView.as_view(), name="asset-detail"),
    path("assets/<int:asset_id>/ping", AssetPingView.as_view(), name="asset-ping"),
]
