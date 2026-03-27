import time

from app.adapter.payment_adapter import SqbPaymentAdapter
from app.protocol.models import (
    CancelRequest,
    OrderQueryRequest,
    PayRequest,
    PrecreateRequest,
    RefundRequest,
)
from app.protocol.parsed_result import ParsedResult
from app.support.polling import build_polling_schedule
from app.support.status_parser import parse_result
from app.support.terminal_credential_store import TerminalCredentialStore


class SqbPaymentFacade:
    def __init__(self, adapter: SqbPaymentAdapter, credential_store: TerminalCredentialStore) -> None:
        self.adapter = adapter
        self.credential_store = credential_store

    def _terminal_key(self, terminal_sn: str) -> str:
        terminal_key = self.credential_store.get_key(terminal_sn)
        if not terminal_key:
            raise ValueError(f"terminal key not found for {terminal_sn}")
        return terminal_key

    def pay_and_poll(self, req: PayRequest, sleep_func=time.sleep) -> ParsedResult:
        terminal_key = self._terminal_key(req.terminal_sn)
        parsed = parse_result(self.adapter.pay(req, terminal_key))
        if parsed.final:
            return parsed

        query_req = OrderQueryRequest(terminal_sn=req.terminal_sn, client_sn=req.client_sn)
        for interval in build_polling_schedule(
            quick_phase_seconds=60,
            quick_interval_seconds=3,
            slow_interval_seconds=10,
            max_wait_seconds=120,
        ):
            sleep_func(interval)
            parsed = parse_result(self.adapter.query(query_req, terminal_key))
            if parsed.final:
                return parsed
        return parsed

    def precreate_and_poll(self, req: PrecreateRequest, sleep_func=time.sleep) -> ParsedResult:
        terminal_key = self._terminal_key(req.terminal_sn)
        parsed = parse_result(self.adapter.precreate(req, terminal_key))
        if parsed.final:
            return parsed

        query_req = OrderQueryRequest(terminal_sn=req.terminal_sn, client_sn=req.client_sn)
        for interval in build_polling_schedule(
            quick_phase_seconds=30,
            quick_interval_seconds=2,
            slow_interval_seconds=5,
            max_wait_seconds=240,
        ):
            sleep_func(interval)
            parsed = parse_result(self.adapter.query(query_req, terminal_key))
            if parsed.final:
                return parsed
        return parsed

    def refund(self, req: RefundRequest) -> ParsedResult:
        terminal_key = self._terminal_key(req.terminal_sn)
        return parse_result(self.adapter.refund(req, terminal_key))

    def cancel(self, req: CancelRequest) -> ParsedResult:
        terminal_key = self._terminal_key(req.terminal_sn)
        return parse_result(self.adapter.cancel(req, terminal_key))
