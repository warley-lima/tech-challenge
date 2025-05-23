from fastapi import FastAPI
from app.routers import api

app = FastAPI(
    title="My hello word",
    version="1.0.0",
    description="API de teste"
)


app.include_router(api.router)