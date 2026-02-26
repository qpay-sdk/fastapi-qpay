from fastapi import Depends
from pydantic import BaseModel
from qpay import AsyncQPayClient, PaymentCheckRequest

from .dependencies import get_qpay_client


class WebhookPayload(BaseModel):
    invoice_id: str


class WebhookResponse(BaseModel):
    status: str
    message: str = ""


async def webhook_handler(
    payload: WebhookPayload,
    client: AsyncQPayClient = Depends(get_qpay_client),
) -> WebhookResponse:
    try:
        result = await client.check_payment(PaymentCheckRequest(
            object_type="INVOICE",
            object_id=payload.invoice_id,
        ))
        if result.rows:
            return WebhookResponse(status="paid", message=f"Payment confirmed for {payload.invoice_id}")
        return WebhookResponse(status="unpaid")
    except Exception as e:
        return WebhookResponse(status="error", message=str(e))
