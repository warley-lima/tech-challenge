from bs4 import BeautifulSoup
import httpx

class HtmlService:
    @staticmethod
    async def get_html(year: int, option: str):
        """
        Função para obter o HTML de uma URL e extrair dados da tabela.
        :param url: URL da página a ser obtida.
        :return: Dados extraídos da tabela.
        """
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
        
        print(f"Buscando URL: {url}") # Para depuração
        try:
             async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', {'class': 'tb_base tb_dados'})
                rows = table.find_all('tr')
                data_json = []
                for row in rows:
                    cells = row.find_all({'th', 'td'})
                    cells_text = [cell.get_text(strip=True) for cell in cells]
                    data_json.append(cells_text)
                return data_json
        except httpx.HTTPStatusError as e:
            return f"Erro HTTP: {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Erro de Requisição: {e}"
        except Exception as e:
            return f"Erro inesperado: {e}"
