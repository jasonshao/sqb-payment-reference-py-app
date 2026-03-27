"""Dependency providers for FastAPI routes."""

from functools import lru_cache

from app.adapter.activate_adapter import SqbActivateAdapter
from app.adapter.base_client import SqbApiClient
from app.adapter.checkin_adapter import SqbCheckinAdapter
from app.adapter.payment_adapter import SqbPaymentAdapter
from app.core.config import Settings
from app.service.notify_handler import SqbNotifyHandler
from app.service.payment_facade import SqbPaymentFacade
from app.support.callback_verifier import SqbCallbackVerifier
from app.support.notify_deduplicator import SqbNotifyDeduplicator
from app.support.terminal_credential_store import TerminalCredentialStore


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_credential_store() -> TerminalCredentialStore:
    return TerminalCredentialStore()


@lru_cache
def get_api_client() -> SqbApiClient:
    return SqbApiClient(get_settings())


@lru_cache
def get_activate_adapter() -> SqbActivateAdapter:
    return SqbActivateAdapter(get_api_client())


@lru_cache
def get_checkin_adapter() -> SqbCheckinAdapter:
    return SqbCheckinAdapter(get_api_client())


@lru_cache
def get_payment_facade() -> SqbPaymentFacade:
    return SqbPaymentFacade(SqbPaymentAdapter(get_api_client()), get_credential_store())


@lru_cache
def get_notify_handler() -> SqbNotifyHandler:
    return SqbNotifyHandler(
        verifier=SqbCallbackVerifier(),
        deduplicator=SqbNotifyDeduplicator(),
        credential_store=get_credential_store(),
    )
