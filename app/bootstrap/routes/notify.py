from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse

from app.bootstrap.dependencies import get_notify_handler
from app.service.notify_handler import SqbNotifyHandler

router = APIRouter(prefix="/notify", tags=["notify"])


@router.post("", response_class=PlainTextResponse)
async def notify(
    request: Request,
    handler: SqbNotifyHandler = Depends(get_notify_handler),
    x_sqb_signature: str = Header(alias="X-SQB-Signature"),
) -> str:
    body = (await request.body()).decode("utf-8")
    ok, message = handler.handle(body, x_sqb_signature)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return "success"
