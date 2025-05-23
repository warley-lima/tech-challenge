import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

class HtmlService:
    @staticmethod
    def get_html(url: str):
        """
        Função para obter o HTML de uma URL e extrair dados da tabela.
        :param url: URL da página a ser obtida.
        :return: Dados extraídos da tabela.
        """
        try:
            response = requests.get(url)
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
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))