from backend.app.core import security


def test_access_token_round_trip():
    token = security.create_access_token({"sub": "soc", "role": "soc"})
    payload = security.decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "soc"
    assert payload["role"] == "soc"


def test_password_hash_and_verify():
    hashed = security.get_password_hash("sentinel-test")
    assert security.verify_password("sentinel-test", hashed) is True
    assert security.verify_password("wrong-password", hashed) is False
