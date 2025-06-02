from typing import Optional
from fastapi import APIRouter, Depends


from app.services.html_service import HtmlService
from app.authentication.router import router as auth_router
from app.authentication.security import get_current_active_user
from app.authentication.schemas import User
from app.services.offline_service import OfflineService
from app.utils.utils import Utils
import json

router = APIRouter()

# Incluíndo as rotas de autenticação
router.include_router(auth_router, tags=["Authentication"])

# Rota para pegar o usuário autenticado
@router.get("/user/auth/", response_model=User, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Rotas protegidas que requerem autenticação
router_protected = APIRouter(
    prefix="/protected",
    tags=["Protected Routes"],
    dependencies=[Depends(get_current_active_user)]
)
@router_protected.get("/ano/{year}/{option}")
async def get_year_option(year: int, option: str, sub_option: Optional[str] = None):
    option = Utils.normalize_option(option)
    sub_option = Utils.normalize_suboption(sub_option)
    response = await HtmlService.get_html(year, option, sub_option)
    return response

@router_protected.get("/offline/ano/{year}/{option}")
async def get_offline_year_option(year: int, option: str, sub_option: Optional[str] = None):
    option = Utils.normalize_option_offline(option)
    response = await OfflineService.get_csv(year, option, sub_option)
    try:
        if response and response != "{}":
            return json.loads(response)
        else:
            return {} 
    except json.JSONDecodeError:
       return {"error": "Falha na conversão JSON interna."}


@router.get("/public/")
async def root():
    response = await HtmlService.get_html('2023', 'opt_02')
    return response 

