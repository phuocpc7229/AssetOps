from django.utils import timezone
from rest_framework import authentication, exceptions

from accounts.models import AccessToken
from accounts.security import hash_access_token


class TokenAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode("utf-8")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Invalid authorization header.")

        token_hash = hash_access_token(parts[1])
        token = AccessToken.objects.select_related("user").filter(token_hash=token_hash).first()
        if token is None:
            raise exceptions.AuthenticationFailed("Invalid access token.")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive.")

        token.last_used_at = timezone.now()
        token.save(update_fields=["last_used_at"])
        return (token.user, token)
