from threading import Lock


class TerminalCredentialStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._keys: dict[str, str] = {}

    def get_key(self, terminal_sn: str) -> str | None:
        with self._lock:
            return self._keys.get(terminal_sn)

    def set_key(self, terminal_sn: str, terminal_key: str) -> None:
        with self._lock:
            self._keys[terminal_sn] = terminal_key
