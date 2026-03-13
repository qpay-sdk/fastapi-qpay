from fastapi import Depends, Query
from fastapi.responses import PlainTextResponse
from qpay import AsyncQPayClient, PaymentCheckRequest

from .dependencies import get_qpay_client


async def webhook_handler(
    qpay_payment_id: str = Query(...),
    client: AsyncQPayClient = Depends(get_qpay_client),
) -> PlainTextResponse:
    """QPay callback handler.

    QPay sends a GET request with ``qpay_payment_id`` as a query parameter.
    The handler verifies the payment via ``check_payment()`` and returns
    ``SUCCESS`` as plain text (HTTP 200).
    """
    await client.check_payment(PaymentCheckRequest(
        object_type="INVOICE",
        object_id=qpay_payment_id,
    ))
    return PlainTextResponse("SUCCESS")
