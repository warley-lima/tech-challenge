from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.authentication.schemas import TokenData, UserInDB, User

# --- Configuração de Segurança ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração OAuth2 para FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

# --- Funções de Hash de Senha ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Funções JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error: Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Mock de usuário temporário para testar a autenticação.
mock_users_db = {
    "user": {
        "username": "user",
        "full_name": "User Test",
        "email": "test@test.com",
        "hashed_password": get_password_hash("123456"), 
        "disabled": False,
    }
}

def get_user(db: dict, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# --- Obter o usuário atual ---
async def authenticate_user(username: str, password: str) -> User | None:
    user = get_user(mock_users_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return User(**user.model_dump()) 

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(mock_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user.model_dump())

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Detail: Inactive user")
    return current_user