"""
Contains the Pydantic models and Enums for the API
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Statistic(str, Enum):
    AVERAGE = "avg"
    MIN = "min"
    MAX = "max"
    SUM = "sum"


class Metric(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"


class SensorData(BaseModel):
    sensor_id: int = Field(ge=0)
    timestamp: datetime
    temperature: float
    humidity: float = Field(ge=0)
    wind_speed: float = Field(ge=0)
