class Utils:

    def normalize_option_offline(option: str) -> str:
        """
        Função para mapear a opção recebida para o formato esperado pelo serviço.
        :param option: Opção recebida na rota.
        :return: Opção mapeada.
        """
        match option:
            case 'producao':
                return 'prod'
            case 'processamento':
                return 'process'
            case 'comercializacao':
                return 'commer'
            case 'importacao':
                return 'import'
            case 'exportacao':
                return 'export'
            case _:
                return 'prod'  # Valor padrão se a opção não for reconhecida
            

    def normalize_option(option: str) -> str:
        """
        Função para mapear a opção recebida para o formato esperado pelo serviço.
        :param option: Opção recebida na rota.
        :return: Opção mapeada.
        """
        match option:
            case 'producao':
                return'opt_02'
            case 'processamento':
                return 'opt_03'
            case 'comercializacao':
                return'opt_04'
            case 'importacao':
                return'opt_05'
            case 'exportacao':
                return 'opt_06'
            case 'publicacao':
                return 'opt_07'
            case _:
                return 'opt_02' # Valor padrão se a opção não for reconhecida   

    def normalize_suboption(suboption: str) -> str:
            """
            Função para mapear a opção recebida para o formato esperado pelo serviço.
            :param option: Opção recebida na rota.
            :return: Opção mapeada.
            """
            print(f"Normalizando subopção: {suboption}")  # Para depuração
            match suboption:
                case 'uvas':
                    return'subopt_03'
                case 'espumantes' | 'americanas':
                    return 'subopt_02'
                case 'vinhos'| 'viniferas':
                    return'subopt_01'
                case 'passas' | 'suco' | 'unclass':
                    return'subopt_04'
                case _:
                    return None # Valor padrão se a sub opção não for reconhecida    
   