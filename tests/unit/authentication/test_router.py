import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.authentication.router import router

client = TestClient(router)

@pytest.fixture
def valid_user():
    class User:
        username = "testuser"
    return User()

@pytest.fixture
def token_response():
    return {"access_token": "fake-token", "token_type": "bearer"}

def test_login_for_access_token_success(valid_user, token_response):
    with patch("app.authentication.router.authenticate_user", new=AsyncMock(return_value=valid_user)) as mock_auth, \
         patch("app.authentication.router.create_access_token", return_value=token_response["access_token"]) as mock_token:
        data = {"username": "testuser", "password": "testpass"}
        response = client.post("/token", data=data)
        assert response.status_code == 200
        assert response.json() == token_response
        mock_auth.assert_awaited_once_with("testuser", "testpass")
        assert mock_token.called

