from app.support.signing import md5_sign


class SqbCallbackVerifier:
    def verify(self, body: str, terminal_key: str, signature: str) -> bool:
        expected = md5_sign(body, terminal_key)
        return expected == signature.lower()
