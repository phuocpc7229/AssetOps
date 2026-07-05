import re
import unicodedata

from rest_framework import serializers

from sites.models import Site


def build_code_from_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().replace("Đ", "D").replace("đ", "d"))
    ascii_value = "".join(character for character in normalized if not unicodedata.combining(character))
    code = re.sub(r"[^0-9A-Za-z]+", "-", ascii_value.upper()).strip("-")
    return re.sub(r"-+", "-", code) or "SITE"


def build_short_site_code_from_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().replace("\u0110", "D").replace("\u0111", "d"))
    ascii_value = "".join(character for character in normalized if not unicodedata.combining(character))
    code = re.sub(r"[^0-9A-Za-z]+", "-", ascii_value.upper()).strip("-")
    return re.sub(r"-+", "-", code) or "SITE"


def build_unique_site_code(name: str) -> str:
    aliases = {
        "HO-CHI-MINH-HEAD-OFFICE": "HCM-HQ",
        "HO-CHI-MINH-HQ": "HCM-HQ",
        "HANOI-BRANCH-01": "HN-BR01",
        "HA-NOI-BRANCH-01": "HN-BR01",
        "DA-NANG-BRANCH-01": "DN-BR01",
        "DA-NANG-OFFICE": "DN-BR01",
    }
    normalized_name = build_short_site_code_from_name(name)
    base_code = aliases.get(normalized_name, normalized_name)[:40]
    code = base_code
    suffix = 2

    while Site.objects.filter(code=code).exists():
        suffix_text = f"-{suffix:02d}"
        code = f"{base_code[:40 - len(suffix_text)]}{suffix_text}"
        suffix += 1

    return code


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "code", "name", "address", "notes", "is_deleted", "deleted_at", "created_at", "updated_at"]
        read_only_fields = ["id", "is_deleted", "deleted_at", "created_at", "updated_at"]
        extra_kwargs = {
            "code": {"validators": [], "required": False, "allow_blank": True},
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
            if self.instance is not None:
                raise serializers.ValidationError("Site code is required.")
            return value
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

    def validate(self, attrs):
        if self.instance is None and not attrs.get("code"):
            name = attrs.get("name", "").strip()
            if name:
                attrs["code"] = build_unique_site_code(name)

        return attrs
