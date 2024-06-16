from fastapi import FastAPI

from app.api.v1.endpoints import health

app = FastAPI()

app.include_router(health.router)