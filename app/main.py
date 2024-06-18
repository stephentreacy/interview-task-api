"""
Main FastAPI application.
"""

from fastapi import FastAPI

from app.api.v1.endpoints import health, query, sensor_data
from app.database import Base, engine

app = FastAPI()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.add_event_handler("startup", create_tables)

app.include_router(health.router)
app.include_router(sensor_data.router)
app.include_router(query.router)
