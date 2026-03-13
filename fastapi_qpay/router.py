from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from qpay import AsyncQPayClient, CreateSimpleInvoiceRequest, PaymentCheckRequest

from .config import QPaySettings, get_settings
from .dependencies import get_qpay_client
from .webhook import webhook_handler


def create_qpay_router(prefix: str = "", tags: list[str] | None = None) -> APIRouter:
    if tags is None:
        tags = ["qpay"]
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("/webhook", response_class=PlainTextResponse)
    async def _webhook(
        qpay_payment_id: str = Query(...),
        client: AsyncQPayClient = Depends(get_qpay_client),
    ):
        return await webhook_handler(qpay_payment_id, client)

    @router.post("/invoice")
    async def _create_invoice(
        sender_invoice_no: str,
        amount: float,
        client: AsyncQPayClient = Depends(get_qpay_client),
        settings: QPaySettings = Depends(get_settings),
    ):
        invoice = await client.create_simple_invoice(CreateSimpleInvoiceRequest(
            invoice_code=settings.invoice_code,
            sender_invoice_no=sender_invoice_no,
            amount=amount,
            callback_url=settings.callback_url,
        ))
        return invoice

    @router.get("/payment/{invoice_id}/status")
    async def _check_payment(
        invoice_id: str,
        client: AsyncQPayClient = Depends(get_qpay_client),
    ):
        result = await client.check_payment(PaymentCheckRequest(
            object_type="INVOICE",
            object_id=invoice_id,
        ))
        return {"paid": len(result.rows) > 0, "rows": result.rows}

    return router


qpay_router = create_qpay_router()
