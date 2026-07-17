"""Unit tests for password hashing and JWT token utilities."""
from datetime import timedelta

from jose import jwt

from app.core import security
from app.core.config import settings


class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        hashed = security.hash_password("Secret@123")
        assert hashed != "Secret@123"

    def test_hash_is_salted_and_unique(self):
        assert security.hash_password("same") != security.hash_password("same")

    def test_verify_correct_password(self):
        hashed = security.hash_password("Secret@123")
        assert security.verify_password("Secret@123", hashed) is True

    def test_verify_wrong_password(self):
        hashed = security.hash_password("Secret@123")
        assert security.verify_password("wrong", hashed) is False


class TestAccessToken:
    def test_create_and_decode_roundtrip(self):
        token = security.create_access_token("user@example.com")
        payload = security.decode_access_token(token)
        assert payload["sub"] == "user@example.com"
        assert "exp" in payload

    def test_token_is_signed_with_configured_algorithm(self):
        token = security.create_access_token("user@example.com")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "user@example.com"

    def test_custom_expiry_is_respected(self):
        short = security.create_access_token("u", expires_delta=timedelta(seconds=1))
        long = security.create_access_token("u", expires_delta=timedelta(days=30))
        assert (
            security.decode_access_token(long)["exp"]
            > security.decode_access_token(short)["exp"]
        )

    def test_decode_invalid_token_returns_none(self):
        assert security.decode_access_token("not-a-real-token") is None

    def test_decode_token_with_wrong_secret_returns_none(self):
        token = jwt.encode({"sub": "u"}, "a-different-secret", algorithm=settings.ALGORITHM)
        assert security.decode_access_token(token) is None

    def test_decode_expired_token_returns_none(self):
        token = security.create_access_token("u", expires_delta=timedelta(seconds=-10))
        assert security.decode_access_token(token) is None
