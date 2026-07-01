from datetime import timedelta

from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_passwors_hash_returns_string():
    password = "mypassword123"
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)


def test_password_hash_is_not_plain():
    password = "mypassword123"
    hashed = get_password_hash(password)
    assert hashed != password


def test_verify_correct_password():
    password = "mypassword123"
    hashed = get_password_hash(password)
    result = verify_password(password, hashed)
    assert result is True


def test_verify_wrong_password():
    password = "mypassword123"
    hashed = get_password_hash(password)
    result = verify_password("wrongpassword", hashed)
    assert result is False


def test_two_hashes_of_same_password_are_different():
    password = "mypassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token_returns_string():
    data = {"sub": "1"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3


def test_decode_valid_token():
    data = {"sub": "42"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"


def test_decode_expired_token():
    data = {"sub": "1"}
    expired_token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    pyload = decode_access_token(expired_token)
    assert pyload == {}


def test_decode_invalid_token():
    fake_token = "this.is.not.a.valid.token"
    payload = decode_access_token(fake_token)
    assert payload == {}
