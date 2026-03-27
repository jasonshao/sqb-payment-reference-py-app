import hashlib
import json
import time
import uuid


def md5_sign(body: str, key: str) -> str:
    return hashlib.md5(f"{body}{key}".encode("utf-8")).hexdigest()


def dumps_body(payload: dict) -> str:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False, sort_keys=True)


def build_authorization(
    *,
    client_sn: str,
    access_token: str,
    signature: str,
    nonce_str: str | None = None,
    timestamp: int | None = None,
) -> str:
    nonce = nonce_str or uuid.uuid4().hex
    ts = timestamp or int(time.time())
    return (
        f'client_sn="{client_sn}",' 
        f'access_token="{access_token}",' 
        f'nonce_str="{nonce}",' 
        f'timestamp="{ts}",' 
        f'sign="{signature}"'
    )
