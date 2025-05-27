# tech-challenge
Project for Tech Challenge fase 1

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

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/protected/ano/2023/producao" \
    -H "Authorization: Bearer <seu_token_aqui>"
```

Lembre-se de substituir `<seu_token_aqui>` pelo token JWT obtido anteriormente.
## Endpoints públicos

Alguns endpoints da API não exigem autenticação e podem ser acessados livremente.

### Exemplo de endpoint público

- **Endpoint:** `GET http://127.0.0.1:8000/public/`

Exemplo de requisição usando `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/public/"
```

A resposta será os dados da produção de 2023 em formato JSON.

