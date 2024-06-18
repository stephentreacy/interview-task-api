"""
Contains endpoint for users to query sensor data.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.data_access import get_sensor_data_statistics
from app.schemas import Metric, Statistic

router = APIRouter(prefix="/api/v1/query", tags=["query"])


@router.get("/")
async def query_sensor_data(
    sensors: list[int] = Query(
        default=None, description="List of sensor IDs, leave empty to query all sensors"
    ),
    metrics: list[Metric] = Query(
        default=None, description="List of metrics, leave empty to query all metrics"
    ),
    statistics: list[Statistic] = Query(
        default=None,
        description="List of statistics to compute, leave empty to get all statistics",
    ),
    time_period: timedelta = Query(
        default=timedelta(days=1),
        description="Time period over which to compute statistics",
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Query sensor data statistics.
    """
    try:
        if not metrics:
            metrics = [*Metric]
        if not statistics:
            statistics = [*Statistic]

        result = await get_sensor_data_statistics(
            db, sensors, metrics, statistics, time_period
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add sensor data.")
