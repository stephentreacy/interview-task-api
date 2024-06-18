"""
Contains functions for the application to interact with the DB.
"""

from datetime import datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_sensor_data(
    db: AsyncSession, sensor_data: schemas.SensorData
) -> models.SensorData:
    """
    Create a new sensor data entry.
    """
    db_sensor_data = models.SensorData(**sensor_data.model_dump())
    db.add(db_sensor_data)
    await db.commit()
    await db.refresh(db_sensor_data)
    return db_sensor_data


async def get_sensor_data_statistics(
    db: AsyncSession,
    sensors: list[int] | None,
    metrics: list[schemas.Metric],
    statistics: list[schemas.Statistic],
    time_period: timedelta,
) -> dict[str, float]:
    """
    Query the database for sensor data statistics.
    """

    selections = []

    # For each statistic call the corresponding SQL function on each metric
    for metric in metrics:
        for statistic in statistics:
            selections.append(
                getattr(func, statistic)(getattr(models.SensorData, metric)).label(
                    f"{metric.value}_{statistic.value}"
                )
            )

    filters = []

    if sensors:
        filters.append(models.SensorData.sensor_id.in_(sensors))

    start_time = datetime.now() - time_period
    filters.append(models.SensorData.timestamp >= start_time)

    query = select(*selections).filter(and_(*filters))

    result = await db.execute(query)
    stats = result.mappings().one()
    return stats
