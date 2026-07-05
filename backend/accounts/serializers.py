from rest_framework import serializers

from accounts.models import AdminUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, trim_whitespace=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "username", "is_active", "is_superuser", "created_at", "updated_at"]
        read_only_fields = fields
