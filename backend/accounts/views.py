from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import AccessToken, AdminUser
from accounts.security import create_access_token, hash_access_token, verify_password
from accounts.serializers import LoginSerializer, SafeUserSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = AdminUser.objects.filter(username=username).first()

        if user is None or not user.is_active or not verify_password(password, user.password_hash):
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = create_access_token()
        AccessToken.objects.create(user=user, token_hash=hash_access_token(token))

        return Response(
            {
                "access_token": token,
                "token_type": "Bearer",
                "user": SafeUserSerializer(user).data,
            }
        )


class MeView(APIView):
    def get(self, request):
        return Response({"user": SafeUserSerializer(request.user).data})
