"""Unit tests for application configuration parsing."""
from app.core.config import Settings, settings


class TestCorsOriginParsing:
    def test_comma_separated_string_is_split(self):
        parsed = Settings.parse_cors_origins("https://a.com, https://b.com")
        assert parsed == ["https://a.com", "https://b.com"]

    def test_single_string_becomes_one_item_list(self):
        assert Settings.parse_cors_origins("https://a.com") == ["https://a.com"]

    def test_whitespace_is_stripped(self):
        assert Settings.parse_cors_origins("  https://a.com  ") == ["https://a.com"]

    def test_list_is_returned_unchanged(self):
        origins = ["https://a.com", "https://b.com"]
        assert Settings.parse_cors_origins(origins) == origins

    def test_string_env_value_parses_into_list(self):
        s = Settings(BACKEND_CORS_ORIGINS="https://x.com,https://y.com")
        assert s.BACKEND_CORS_ORIGINS == ["https://x.com", "https://y.com"]


class TestDefaults:
    def test_default_algorithm(self):
        assert settings.ALGORITHM == "HS256"

    def test_api_prefix(self):
        assert settings.API_V1_STR == "/api"

    def test_token_expiry_default(self):
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 1440
