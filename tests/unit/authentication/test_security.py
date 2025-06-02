import pytest
from fastapi import HTTPException, status
from jose import jwt
from datetime import timedelta, datetime, timezone
from unittest.mock import patch, MagicMock, AsyncMock
from app.authentication import security
from app.authentication.schemas import UserInDB, User, TokenData

@pytest.fixture
def password():
    return "mysecret"

@pytest.fixture
def hashed_password(password):
    return security.get_password_hash(password)

def test_verify_password_success(password, hashed_password):
    assert security.verify_password(password, hashed_password)

def test_verify_password_fail():
    hash_pw = security.get_password_hash("abc")
    assert not security.verify_password("wrong", hash_pw)

def test_get_password_hash(password):
    hashed = security.get_password_hash(password)
    assert isinstance(hashed, str)
    assert security.verify_password(password, hashed)

def test_create_and_decode_access_token():
    data = {"sub": "user"}
    token = security.create_access_token(data, expires_delta=timedelta(minutes=5))
    payload = security.decode_access_token(token)
    assert payload["sub"] == "user"
    assert "exp" in payload

def test_decode_access_token_invalid():
    with pytest.raises(HTTPException) as exc:
        security.decode_access_token("invalid.token.value")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_user_found():
    db = {"foo": {"username": "foo", "full_name": "Foo", "email": "foo@bar.com", "hashed_password": security.get_password_hash("pw"), "disabled": False}}
    user = security.get_user(db, "foo")
    assert isinstance(user, UserInDB)
    assert user.username == "foo"

def test_get_user_not_found():
    db = {}
    user = security.get_user(db, "bar")
    assert user is None

@pytest.mark.asyncio
async def test_authenticate_user_success():
    username = "user"
    password = "123456"
    user = await security.authenticate_user(username, password)
    assert isinstance(user, User)
    assert user.username == username

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    user = await security.authenticate_user("user", "wrongpw")
    assert user is None

@pytest.mark.asyncio
async def test_authenticate_user_wrong_username():
    user = await security.authenticate_user("notfound", "123456")
    assert user is None

@pytest.mark.asyncio
async def test_get_current_user_success(monkeypatch):
    user = UserInDB(username="user", full_name="User Test", email="test@test.com", hashed_password="x", disabled=False)
    token = security.create_access_token({"sub": "user"})
    monkeypatch.setattr(security, "decode_access_token", lambda t: {"sub": "user"})
    monkeypatch.setattr(security, "get_user", lambda db, username: user)
    result = await security.get_current_user(token)
    assert isinstance(result, User)
    assert result.username == "user"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(monkeypatch):
    monkeypatch.setattr(security, "decode_access_token", lambda t: (_ for _ in ()).throw(HTTPException(status_code=401)))
    with pytest.raises(HTTPException):
        await security.get_current_user("badtoken")

@pytest.mark.asyncio
async def test_get_current_user_missing_username(monkeypatch):
    monkeypatch.setattr(security, "decode_access_token", lambda t: {})
    with pytest.raises(HTTPException):
        await security.get_current_user("token")

@pytest.mark.asyncio
async def test_get_current_user_user_not_found(monkeypatch):
    monkeypatch.setattr(security, "decode_access_token", lambda t: {"sub": "nouser"})
    monkeypatch.setattr(security, "get_user", lambda db, username: None)
    with pytest.raises(HTTPException):
        await security.get_current_user("token")

@pytest.mark.asyncio
async def test_get_current_active_user_active(monkeypatch):
    user = User(username="user", full_name="User Test", email="test@test.com", disabled=False)
    result = await security.get_current_active_user(user)
    assert result == user

@pytest.mark.asyncio
async def test_get_current_active_user_disabled():
    user = User(username="user", full_name="User Test", email="test@test.com", disabled=True)
    with pytest.raises(HTTPException) as exc:
        await security.get_current_active_user(user)
    assert exc.value.status_code == 400