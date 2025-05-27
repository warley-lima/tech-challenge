from fastapi import APIRouter, Depends


from app.services.html_service import HtmlService
from app.authentication.router import router as auth_router
from app.authentication.security import get_current_active_user
from app.authentication.schemas import User
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
async def get_year(year: int, option: str):
    match option:
        case 'producao':
            option = 'opt_02'
        case 'processamento':
            option = 'opt_03'
        case 'comercializacao':
            option = 'opt_04'
        case 'importacao':
            option = 'opt_05'
        case 'exportacao':
            option = 'opt_06'
        case 'publicacao':
            option = 'opt_07'
        case _:
            option = 'opt_02'
    response = await HtmlService.get_html(year, option)
    return response

@router.get("/public/")
async def root():
    response = await HtmlService.get_html('2023', 'opt_02')
    return response 

