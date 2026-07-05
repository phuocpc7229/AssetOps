from django.urls import include, path

from accounts.views import ChangePasswordView, LoginView, MeView
from health.views import HealthView


urlpatterns = [
    path("api/v1/health", HealthView.as_view(), name="health"),
    path("api/v1/auth/login", LoginView.as_view(), name="auth-login"),
    path("api/v1/auth/me", MeView.as_view(), name="auth-me"),
    path("api/v1/auth/change-password", ChangePasswordView.as_view(), name="auth-change-password"),
    path("api/v1/", include("assets.urls")),
    path("api/v1/", include("dashboard.urls")),
    path("api/v1/", include("sites.urls")),
]
