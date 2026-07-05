from django.urls import path

from accounts.views import LoginView, MeView
from health.views import HealthView


urlpatterns = [
    path("api/v1/health", HealthView.as_view(), name="health"),
    path("api/v1/auth/login", LoginView.as_view(), name="auth-login"),
    path("api/v1/auth/me", MeView.as_view(), name="auth-me"),
]
