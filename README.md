# tech-challenge
Project for Tech Challenge fase 1

# Tech Challenge - API Vitibrasil

Este projeto é uma API desenvolvida em FastAPI para consulta de dados públicos do sistema Vitibrasil (Embrapa), com autenticação JWT, endpoints protegidos e suporte a leitura de dados offline (CSV).

## Funcionalidades

- **Autenticação JWT**: Geração e validação de tokens de acesso.
- **Endpoints protegidos**: Rotas que exigem autenticação para acesso.
- **Consulta de dados online**: Busca e extração de tabelas HTML do site da Embrapa.
- **Consulta de dados offline**: Leitura de arquivos CSV locais quando o sistema online estiver indisponível.
- **Normalização de parâmetros**: Utilitários para padronizar opções e subopções de consulta.

## Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repo>
   cd tech-challenge

## Como obter o token de autenticação

Para acessar a API, é necessário autenticar-se e obter um token JWT.

- **Endpoint:** `POST http://127.0.0.1:8000/token`
- **Usuário:** `user`
- **Senha:** `123456`

Exemplo de requisição usando `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=user&password=123456"
```

A resposta será um JSON contendo o token de acesso:

```json
{
    "access_token": "<seu_token_aqui>",
    "token_type": "bearer"
}
```
## Autenticando com o token

Após obter o token de acesso, inclua-o no cabeçalho `Authorization` das suas requisições para acessar os endpoints protegidos da API.

Exemplo de requisição autenticada usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/user/auth/" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

Substitua `<seu_token_aqui>` pelo token recebido na etapa anterior.
## Endpoint protegido: Obter informações por ano

Para acessar informações específicas de um determinado ano, utilize o endpoint protegido abaixo. É necessário incluir o token de autenticação no cabeçalho da requisição.
As opções diponíveis são: producao, processamento, comercializacao, importacao, exportacao, publicacao

- **Endpoint:** `GET http://127.0.0.1:8000/protected/ano/{year}/{option}`

Substitua `{year}` pelo ano desejado (ex: `2023`) e `{option}` pela opção correspondente.
As opções disponíveis para o endpoint sâo: producao, processamento, comercializacao, importacao, exportacao.

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/protected/ano/2023/producao" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

Lembre-se de substituir `<seu_token_aqui>` pelo token JWT obtido anteriormente.

Também é possível consultar as informações das subopções, são elas: uvas, espumantes, americanas, vinhos, viniferas, passas, suco, unclass.

- **Endpoint:** `GET http://127.0.0.1:8000/protected/ano/{year}/{option}?{sub_option}`

Substitua `{year}` pelo ano desejado (ex: `2022`) e `{option}` pela opção correspondente.
As opções disponíveis para o endpoint sâo: processamento, importacao, exportacao; e `{sub_option}` pela subopção correspondente, são elas: uvas, espumantes, americanas, vinhos, viniferas, passas, suco, unclass. 

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/protected/ano/2022/exportacao?sub_option=uvas" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

## Endpoint: `/protected/offline/ano/{year}/{option}`

Este endpoint permite consultar dados offline (arquivos CSV locais) de acordo com o ano e a opção informados, sendo protegido por autenticação JWT, retornando o json do CSV lido, ou as mensagens de erro caso algum problema aconteça. Substitua `{year}` pelo ano desejado (ex: `2022`) e `{option}` pela opção correspondente. As opções disponíveis são: producao, comercializacao.

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/protected/offline/ano/2022/producao" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

## Endpoint: `/protected/offline/ano/{year}/{option}?{sub_option}`

Este endpoint permite consultar dados offline (arquivos CSV locais) de acordo com o ano e a opção informados, sendo protegido por autenticação JWT, retornando o json do CSV lido, ou as mensagens de erro caso algum problema aconteça. Substitua `{year}` pelo ano desejado (ex: `2022`) e `{option}` e `{sub_option}` pela opção correspondente. As opções disponíveis são: processamento,  importacao, exportacao. E as subopções disponíveis são: uvas, espumantes, americanas, vinhos, viniferas, passas, suco, unclass.

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/protected/offline/ano/2022/exportacao?sub_option=suco" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

## Endpoints públicos

Alguns endpoints da API não exigem autenticação e podem ser acessados livremente.

### Exemplo de endpoint público

- **Endpoint:** `GET http://127.0.0.1:8000/public/`

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/public/"
```

A resposta será os dados da produção de 2023 em formato JSON.

