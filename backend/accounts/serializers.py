from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accounts.models import AdminUser
from accounts.security import verify_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, trim_whitespace=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "username", "is_active", "is_superuser", "created_at", "updated_at"]
        read_only_fields = fields


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_current_password(self, value):
        user = self.context["user"]
        if not verify_password(value, user.password_hash):
            raise serializers.ValidationError("Current password is incorrect.")

        return value

    def validate(self, attrs):
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "New password and confirmation do not match."})

        try:
            validate_password(new_password, user=self.context["user"])
        except DjangoValidationError as error:
            raise serializers.ValidationError({"new_password": list(error.messages)}) from error

        return attrs
