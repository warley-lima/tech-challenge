import pandas as pd
import os

class OfflineService:
    async def get_csv(year: int, dir: str, subDir: str):
        """
         Método para ler os dados localmente, quando o sistema da embrapa estiver indi.
        :param url: URL da página a ser obtida.
        :return: Dados extraídos da tabela.
        """
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_app = os.path.dirname(dir_atual)
        dir_root_proj = os.path.dirname(dir_app)
        if subDir is None:
            subDir = ''
        
        path_data = os.path.join(dir_root_proj, 'data', dir, subDir)
        name_file_csv = f"{year}.csv"
        path_csv = os.path.join(path_data,  name_file_csv) 
        try:
            df = pd.read_csv(path_csv, sep=';', skiprows=0, encoding='utf-8', engine='python') 
            return df.to_json(orient='records', indent=1, force_ascii=False)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{path_csv}' não foi encontrado em '{path_data}'.")
            return "Arquivo não encontrado"
        except pd.errors.EmptyDataError:
            print(f"Erro: O arquivo CSV '{path_csv}' está vazio ou não possui cabeçalho/dados.")
            return "Arquivo vazio ou sem dados"
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
            return "Ocorreu um erro inesperado ao ler o arquivo"