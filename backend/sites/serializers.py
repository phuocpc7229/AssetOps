from rest_framework import serializers

from sites.models import Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "code", "name", "address", "notes", "is_deleted", "deleted_at", "created_at", "updated_at"]
        read_only_fields = ["id", "is_deleted", "deleted_at", "created_at", "updated_at"]
        extra_kwargs = {
            "code": {"validators": []},
            "address": {
                "error_messages": {
                    "blank": "Site address is required.",
                    "required": "Site address is required.",
                }
            },
        }

    def validate_code(self, value):
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError("Site code is required.")
        existing = Site.objects.filter(code=value)
        if self.instance is not None:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError("A site with this code already exists.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Site name is required.")
        return value

    def validate_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Site address is required.")
        return value
