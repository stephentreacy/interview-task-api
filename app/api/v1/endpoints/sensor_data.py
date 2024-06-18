"""
Contains endpoint for sensors to interact with the application.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import data_access, schemas
from app.api.v1.dependencies import get_db

router = APIRouter(prefix="/api/v1/sensor-data", tags=["sensor-data"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_sensor_data(
    sensor_data: schemas.SensorData, db: AsyncSession = Depends(get_db)
) -> schemas.SensorData:
    """
    Create a new sensor data entry.
    """
    try:
        result = await data_access.create_sensor_data(db=db, sensor_data=sensor_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add sensor data.")
