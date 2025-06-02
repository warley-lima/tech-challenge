import pytest
from unittest.mock import patch
from fastapi import status, FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient

from app.routers.api import router 
from app.authentication.security import get_current_active_user 
from app.authentication.schemas import User

# --- Fixtures ---

@pytest.fixture
def test_user():
    """Fixture para um usuário de teste ativo."""
    # Garanta que o User schema tenha 'id' se estiver usando no Pydantic model
    return User(id=1, username="testuser", email="test@example.com", is_active=True)

@pytest.fixture
def app_with_overrides():
    """
    Fixture que retorna uma nova instância do FastAPI,
    permitindo que as dependências sejam sobrescritas por teste.
    """
    app_test = FastAPI()
    app_test.include_router(router) # Inclua o seu router principal aqui
    yield app_test
    # Limpa as sobrescrições após cada teste para evitar vazamentos entre testes
    app_test.dependency_overrides.clear()

@pytest.fixture
def client_authenticated(app_with_overrides: FastAPI, test_user: User):
    """
    Fixture para um TestClient com um usuário autenticado mockado.
    """
    # Sobrescreve a dependência específica para esta instância do FastAPI
    # A função lambda garante que 'test_user' seja capturado no contexto do teste
    app_with_overrides.dependency_overrides[get_current_active_user] = lambda: test_user
    
    with TestClient(app_with_overrides) as c:
        yield c

# --- Testes ---

def test_read_users_me_authenticated_fixture(client_authenticated: TestClient, test_user: User):
    """
    Testa a rota '/user/auth/' quando o usuário está autenticado usando a fixture.
    """
    response = client_authenticated.get("/user/auth/")
    print(response.json()) # Para depuração
    
    assert response.status_code == status.HTTP_200_OK
    # Use .model_dump() para comparar o Pydantic model com o JSON retornado
    assert response.json() == test_user.model_dump() 
