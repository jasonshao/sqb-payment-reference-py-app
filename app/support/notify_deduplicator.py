from threading import Lock


class SqbNotifyDeduplicator:
    def __init__(self) -> None:
        self._seen: set[str] = set()
        self._lock = Lock()

    def is_duplicate(self, dedup_key: str) -> bool:
        with self._lock:
            if dedup_key in self._seen:
                return True
            self._seen.add(dedup_key)
            return False
