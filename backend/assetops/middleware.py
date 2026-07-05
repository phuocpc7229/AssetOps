from django.conf import settings
from django.http import HttpResponse


class CorsMiddleware:
    allowed_headers = "authorization,content-type"
    allowed_methods = "GET,POST,PUT,PATCH,DELETE,OPTIONS"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        if request.method == "OPTIONS" and self._is_allowed_origin(origin):
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if self._is_allowed_origin(origin):
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Headers"] = self.allowed_headers
            response["Access-Control-Allow-Methods"] = self.allowed_methods

        return response

    @staticmethod
    def _is_allowed_origin(origin: str | None) -> bool:
        return bool(origin and origin in settings.CORS_ALLOWED_ORIGINS)
