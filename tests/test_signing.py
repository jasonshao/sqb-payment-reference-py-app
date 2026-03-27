from app.support.signing import build_authorization, md5_sign


def test_md5_sign_is_lowercase_32_hex() -> None:
    assert md5_sign("{}", "abc") == "99914b932bd37a50b983c5e7c90ae93b"


def test_build_authorization_contains_required_fields() -> None:
    header = build_authorization(
        client_sn="c1",
        access_token="t1",
        signature="s1",
        nonce_str="n1",
        timestamp=1,
    )
    assert 'client_sn="c1"' in header
    assert 'access_token="t1"' in header
    assert 'nonce_str="n1"' in header
    assert 'timestamp="1"' in header
    assert 'sign="s1"' in header
