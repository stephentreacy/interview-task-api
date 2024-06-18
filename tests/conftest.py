"""
Set up test databse and pytest fixtures for tests.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import models, schemas
from app.api.v1.dependencies import get_db
from app.database import Base
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def overide_database():
    async def test_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = test_get_db


@pytest.fixture(autouse=True)
async def refresh_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def data_prepared_db():
    async with TestingSessionLocal() as session:
        sample_data = [
            schemas.SensorData(
                sensor_id=1,
                timestamp=datetime(2020, 1, 10),
                temperature=0,
                humidity=0,
                wind_speed=0,
            ),
            schemas.SensorData(
                sensor_id=1,
                timestamp=datetime(2020, 1, 10),
                temperature=20.0,
                humidity=100.0,
                wind_speed=3.0,
            ),
            schemas.SensorData(
                sensor_id=1,
                timestamp=datetime(2020, 1, 1),
                temperature=10.0,
                humidity=40.0,
                wind_speed=5.0,
            ),
            schemas.SensorData(
                sensor_id=2,
                timestamp=datetime(2020, 1, 10),
                temperature=0,
                humidity=0,
                wind_speed=0,
            ),
        ]

        for data in sample_data:
            db_sensor_data = models.SensorData(**data.model_dump())
            session.add(db_sensor_data)
            await session.commit()


@pytest.fixture()
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
def client():
    """
    Fixture that provides a test client for the FastAPI app.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sensor_data_payload():
    """
    Example of a valid sensor data payload
    """
    return {
        "sensor_id": 1,
        "timestamp": "2024-06-16T12:59:00.863000",
        "temperature": 22.5,
        "humidity": 55.0,
        "wind_speed": 5.5,
    }
