from fastapi import APIRouter


from app.services.html_service import HtmlService
router = APIRouter()


@router.get("/ano/{year}/{option}")
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

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
    response = HtmlService.get_html(url)
    return response

@router.get("/")
async def root():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_02"
    response = HtmlService.get_html(url)
    return response 

