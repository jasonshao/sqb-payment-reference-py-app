import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class SqbCallbackVerifier:
    def __init__(self, public_key_pem: str) -> None:
        self.public_key = None
        if public_key_pem.strip():
            self.public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))

    def verify(self, body: str, signature: str) -> bool:
        if self.public_key is None:
            return False

        encoded_signature = signature.strip().split()[-1]
        try:
            self.public_key.verify(
                base64.b64decode(encoded_signature),
                body.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except (InvalidSignature, ValueError, TypeError):
            return False
        return True
