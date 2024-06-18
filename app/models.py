"""
Contains the SQLAlchemy models for the application.
"""

from sqlalchemy import Column, DateTime, Float, Integer

from app.database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
