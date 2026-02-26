from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from qpay import QPayConfig


class QPaySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QPAY_", env_file=".env", extra="ignore")

    base_url: str = "https://merchant.qpay.mn"
    username: str = ""
    password: str = ""
    invoice_code: str = ""
    callback_url: str = ""

    def to_qpay_config(self) -> QPayConfig:
        return QPayConfig(
            base_url=self.base_url,
            username=self.username,
            password=self.password,
            invoice_code=self.invoice_code,
            callback_url=self.callback_url,
        )


@lru_cache
def get_settings() -> QPaySettings:
    return QPaySettings()
