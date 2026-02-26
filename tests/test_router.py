from fastapi import APIRouter

from fastapi_qpay.router import create_qpay_router, qpay_router


class TestCreateQPayRouter:
    def test_returns_api_router(self):
        router = create_qpay_router()
        assert isinstance(router, APIRouter)

    def test_default_tags(self):
        router = create_qpay_router()
        assert router.tags == ["qpay"]

    def test_custom_prefix(self):
        router = create_qpay_router(prefix="/payments")
        assert router.prefix == "/payments"

    def test_custom_tags(self):
        router = create_qpay_router(tags=["billing"])
        assert router.tags == ["billing"]

    def test_has_routes(self):
        router = create_qpay_router()
        paths = [route.path for route in router.routes]
        assert "/webhook" in paths
        assert "/invoice" in paths
        assert "/payment/{invoice_id}/status" in paths


class TestDefaultRouter:
    def test_qpay_router_is_api_router(self):
        assert isinstance(qpay_router, APIRouter)

    def test_qpay_router_has_routes(self):
        paths = [route.path for route in qpay_router.routes]
        assert len(paths) >= 3
