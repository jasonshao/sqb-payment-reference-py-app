"""FastAPI application entrypoint."""

from fastapi import Depends, FastAPI

from app.bootstrap.dependencies import get_settings
from app.bootstrap.routes.notify import router as notify_router
from app.bootstrap.routes.payment import router as payment_router
from app.bootstrap.routes.terminal import router as terminal_router
from app.core.config import Settings

app = FastAPI(title="SQB Payment Reference Python App", version="0.2.0")
app.include_router(terminal_router)
app.include_router(payment_router)
app.include_router(notify_router)


@app.get("/health")
def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }
