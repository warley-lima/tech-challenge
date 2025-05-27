from fastapi import FastAPI
from app.routers import api

app = FastAPI(
    title="Web-scraping API",
    version="1.0.1",
    description="API para web-scraping de dados do site vitibrasil.cnpuv.embrapa.br",
    docs_url="/docs",
)


app.include_router(api.router)
app.include_router(api.router_protected)