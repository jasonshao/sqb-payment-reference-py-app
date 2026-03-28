from app.support.signing import build_authorization, md5_sign


def test_md5_sign_is_lowercase_32_hex() -> None:
    assert md5_sign("{}", "abc") == "99914b932bd37a50b983c5e7c90ae93b"


def test_build_authorization_contains_required_fields() -> None:
    header = build_authorization(signatory_sn="c1", signature="s1")
    assert header == "c1 s1"
