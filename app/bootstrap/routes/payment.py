from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.dependencies import get_payment_facade
from app.protocol.models import CancelRequest, PayRequest, PrecreateRequest, RefundRequest
from app.service.payment_facade import SqbPaymentFacade

router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/pay")
def pay(req: PayRequest, facade: SqbPaymentFacade = Depends(get_payment_facade)) -> dict:
    try:
        result = facade.pay_and_poll(req, sleep_func=lambda _: None)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": result.order_status, "final": result.final, "success": result.success}


@router.post("/precreate")
def precreate(req: PrecreateRequest, facade: SqbPaymentFacade = Depends(get_payment_facade)) -> dict:
    try:
        result = facade.precreate_and_poll(req, sleep_func=lambda _: None)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": result.order_status, "final": result.final, "success": result.success}


@router.post("/refund")
def refund(req: RefundRequest, facade: SqbPaymentFacade = Depends(get_payment_facade)) -> dict:
    try:
        result = facade.refund(req)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": result.order_status, "final": result.final, "success": result.success}


@router.post("/cancel")
def cancel(req: CancelRequest, facade: SqbPaymentFacade = Depends(get_payment_facade)) -> dict:
    try:
        result = facade.cancel(req)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": result.order_status, "final": result.final, "success": result.success}
