from unittest.mock import patch

from fastapi_qpay.config import QPaySettings, get_settings


class TestQPaySettings:
    def test_default_values(self):
        with patch.dict("os.environ", {}, clear=True):
            settings = QPaySettings(
                base_url="https://merchant.qpay.mn",
                username="",
                password="",
                invoice_code="",
                callback_url="",
            )
            assert settings.base_url == "https://merchant.qpay.mn"
            assert settings.username == ""
            assert settings.password == ""
            assert settings.invoice_code == ""
            assert settings.callback_url == ""

    def test_from_env_variables(self):
        env = {
            "QPAY_BASE_URL": "https://merchant-sandbox.qpay.mn",
            "QPAY_USERNAME": "test_user",
            "QPAY_PASSWORD": "test_pass",
            "QPAY_INVOICE_CODE": "TEST_CODE",
            "QPAY_CALLBACK_URL": "https://example.com/callback",
        }
        with patch.dict("os.environ", env, clear=True):
            settings = QPaySettings()
            assert settings.base_url == "https://merchant-sandbox.qpay.mn"
            assert settings.username == "test_user"
            assert settings.password == "test_pass"
            assert settings.invoice_code == "TEST_CODE"
            assert settings.callback_url == "https://example.com/callback"

    def test_to_qpay_config(self):
        settings = QPaySettings(
            base_url="https://merchant-sandbox.qpay.mn",
            username="user",
            password="pass",
            invoice_code="INV",
            callback_url="https://example.com/cb",
        )
        config = settings.to_qpay_config()
        assert config.base_url == "https://merchant-sandbox.qpay.mn"
        assert config.username == "user"
        assert config.password == "pass"
        assert config.invoice_code == "INV"
        assert config.callback_url == "https://example.com/cb"


class TestGetSettings:
    def test_returns_qpay_settings(self):
        get_settings.cache_clear()
        env = {
            "QPAY_USERNAME": "cached_user",
            "QPAY_PASSWORD": "cached_pass",
        }
        with patch.dict("os.environ", env, clear=True):
            result = get_settings()
            assert isinstance(result, QPaySettings)
            assert result.username == "cached_user"
        get_settings.cache_clear()

    def test_is_cached(self):
        get_settings.cache_clear()
        env = {
            "QPAY_USERNAME": "user1",
            "QPAY_PASSWORD": "pass1",
        }
        with patch.dict("os.environ", env, clear=True):
            first = get_settings()
            second = get_settings()
            assert first is second
        get_settings.cache_clear()
