# fastapi-qpay

[![PyPI](https://img.shields.io/pypi/v/fastapi-qpay)](https://pypi.org/project/fastapi-qpay/)
[![CI](https://github.com/qpay-sdk/fastapi-qpay/actions/workflows/ci.yml/badge.svg)](https://github.com/qpay-sdk/fastapi-qpay/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

QPay V2 payment integration for FastAPI.

## Install

```bash
pip install fastapi-qpay
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi_qpay import qpay_router

app = FastAPI()
app.include_router(qpay_router, prefix="/qpay")
```

## Configuration

```bash
QPAY_BASE_URL=https://merchant.qpay.mn
QPAY_USERNAME=your_username
QPAY_PASSWORD=your_password
QPAY_INVOICE_CODE=your_invoice_code
QPAY_CALLBACK_URL=https://yoursite.com/qpay/webhook
```

## Dependency Injection

```python
from fastapi import Depends
from qpay import AsyncQPayClient
from fastapi_qpay import get_qpay_client

@app.post("/pay")
async def pay(client: AsyncQPayClient = Depends(get_qpay_client)):
    invoice = await client.create_simple_invoice(...)
    return invoice
```

## License

MIT
