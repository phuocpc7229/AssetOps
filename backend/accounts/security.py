import hashlib
import secrets

from django.contrib.auth.hashers import check_password, make_password


def hash_password(raw_password: str) -> str:
    return make_password(raw_password)


def verify_password(raw_password: str, password_hash: str) -> bool:
    return check_password(raw_password, password_hash)


def create_access_token() -> str:
    return secrets.token_urlsafe(48)


def hash_access_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
