
import pytest
from unittest.mock import AsyncMock, patch


from app.services.html_service import HtmlService
from httpx import HTTPStatusError, Request, Response, RequestError

@pytest.mark.asyncio
async def test_get_html_success():
    """
    Testa se a função get_html retorna os dados corretos em caso de sucesso.
    """
    
    mock_html = """
    <html>
        <body>
            <table class="tb_base tb_dados">
                <tr><th>Header test 1</th><th>Header test 2</th></tr>
                <tr><td>Data test 1</td><td>Data test 1B</td></tr>
                <tr><td>Data test 2</td><td>Data test 2B</td></tr>
            </table>
        </body>
    </html>
    """
    
    expected_data = [
        ['Header test 1', 'Header test 2'],
        ['Data test 1', 'Data test 1B'],
        ['Data test 2', 'Data test 2B']
    ]

    with patch('httpx.AsyncClient') as mock_async_client:
        mock_response = AsyncMock()
        mock_response.text = mock_html
        
        mock_async_client.return_value.__aenter__.return_value.get.return_value = mock_response

        result = await HtmlService.get_html(year=2023, option="producao")

        mock_async_client.return_value.__aenter__.return_value.get.assert_called_once_with(
            "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=producao", follow_redirects=True
        )

        assert result == expected_data



@pytest.mark.asyncio
async def test_get_html_http_status_error():
    """
    Teste para o httpx.HTTPStatusError
    simulando a exceção diretamente no 'get'.
    """
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_request = Request("GET", "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=20210&opcao=comercializacao")
        
        mock_error_response = Response(status_code=400, request=mock_request, text="Bad Request Details")

        mock_async_client.return_value.__aenter__.return_value.get.side_effect = HTTPStatusError(
            "Bad Request", 
            request=mock_request, 
            response=mock_error_response
        )

        result = await HtmlService.get_html(year=20210, option="comercializacao")

        assert "Erro HTTP: 400 - Bad Request Details" in result

@pytest.mark.asyncio
async def test_get_html_request_error():
    """
    Teste para verificar httpx.RequestError.
    """
    
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.side_effect = RequestError(
            "Network Error", request=AsyncMock()
        )

        result = await HtmlService.get_html(year=2023, option="importacao")
        assert "Erro de Requisição: Network Error" in result

@pytest.mark.asyncio
async def test_get_html_parsing_error():
    """
    Teste nos casos de erros de parsing (ex: tabela não encontrada).
    """
    
    mock_html_no_table = """
    <html>
        <body>
            <div>No relevant table here</div>
        </body>
    </html>
    """
    
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_response = AsyncMock()
        mock_response.text = mock_html_no_table
        mock_async_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        result = await HtmlService.get_html(year=2023, option="exportacao")

        assert "Erro inesperado: 'NoneType' object has no attribute 'find_all'" in result       


   