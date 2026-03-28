import hashlib
import json


def md5_sign(body: str, key: str) -> str:
    return hashlib.md5(f"{body}{key}".encode("utf-8")).hexdigest()


def dumps_body(payload: dict) -> str:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False, sort_keys=True)


def build_authorization(*, signatory_sn: str, signature: str) -> str:
    return f"{signatory_sn} {signature}"
