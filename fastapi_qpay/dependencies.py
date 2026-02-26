from typing import AsyncGenerator

from fastapi import Depends
from qpay import AsyncQPayClient, QPayConfig

from .config import QPaySettings, get_settings


def get_qpay_config(settings: QPaySettings = Depends(get_settings)) -> QPayConfig:
    return settings.to_qpay_config()


async def get_qpay_client(config: QPayConfig = Depends(get_qpay_config)) -> AsyncGenerator[AsyncQPayClient, None]:
    client = AsyncQPayClient(config)
    try:
        yield client
    finally:
        await client.close()
