from fastapi import APIRouter, Depends, HTTPException

from app.adapter.activate_adapter import SqbActivateAdapter
from app.adapter.checkin_adapter import SqbCheckinAdapter
from app.bootstrap.dependencies import (
    get_activate_adapter,
    get_checkin_adapter,
    get_credential_store,
)
from app.protocol.models import ActivateRequest, ActivateResponse, CheckinRequest, CheckinResponse
from app.support.terminal_credential_store import TerminalCredentialStore

router = APIRouter(prefix="/terminal", tags=["terminal"])


@router.post("/activate", response_model=ActivateResponse)
def activate(
    req: ActivateRequest,
    adapter: SqbActivateAdapter = Depends(get_activate_adapter),
    store: TerminalCredentialStore = Depends(get_credential_store),
) -> ActivateResponse:
    resp = adapter.activate(req)
    terminal_key = resp.get("biz_response", {}).get("terminal_key", f"key-{req.terminal_sn}")
    store.set_key(req.terminal_sn, terminal_key)
    return ActivateResponse(terminal_sn=req.terminal_sn, terminal_key=terminal_key)


@router.post("/checkin", response_model=CheckinResponse)
def checkin(
    req: CheckinRequest,
    adapter: SqbCheckinAdapter = Depends(get_checkin_adapter),
    store: TerminalCredentialStore = Depends(get_credential_store),
) -> CheckinResponse:
    terminal_key = store.get_key(req.terminal_sn)
    if not terminal_key:
        raise HTTPException(status_code=404, detail="terminal not activated")

    resp = adapter.checkin(req, terminal_key)
    updated_key = resp.get("biz_response", {}).get("terminal_key", terminal_key)
    store.set_key(req.terminal_sn, updated_key)
    return CheckinResponse(terminal_sn=req.terminal_sn, terminal_key=updated_key)
