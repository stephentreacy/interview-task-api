from datetime import timedelta

import pytest
from freezegun import freeze_time
from sqlalchemy import select

from app import data_access, schemas
from app.models import SensorData

pytestmark = pytest.mark.anyio


async def test_create_sensor_data(db_session, sensor_data_payload):
    """
    Test that data is added to the darabase.
    """
    sensor_data = schemas.SensorData(**sensor_data_payload)

    created_sensor_data = await data_access.create_sensor_data(db_session, sensor_data)

    query = select(SensorData)
    result = await db_session.execute(query)
    db_sensor_data = result.scalars().first()
    assert db_sensor_data.temperature == sensor_data.temperature
    assert db_sensor_data.humidity == sensor_data.humidity
    assert db_sensor_data.wind_speed == sensor_data.wind_speed
    assert db_sensor_data.timestamp == sensor_data.timestamp


@pytest.mark.parametrize(
    "sensors, metrics, statistics, time_period, expected_output",
    [
        # Test case 1: Get everything for the last day
        (
            None,
            [*schemas.Metric],
            [*schemas.Statistic],
            timedelta(days=1),
            {
                "temperature_avg": 6.666666666666667,
                "temperature_min": 0.0,
                "temperature_max": 20.0,
                "temperature_sum": 20.0,
                "humidity_avg": 33.333333333333336,
                "humidity_min": 0.0,
                "humidity_max": 100.0,
                "humidity_sum": 100.0,
                "wind_speed_avg": 1.0,
                "wind_speed_min": 0.0,
                "wind_speed_max": 3.0,
                "wind_speed_sum": 3.0,
            },
        ),
        # Test Case 2: Get max of all metrics for the last 2 weeks
        (
            [1],
            [*schemas.Metric],
            [schemas.Statistic.MAX],
            timedelta(weeks=2),
            {
                "temperature_max": 20.0,
                "humidity_max": 100.0,
                "wind_speed_max": 5.0,
            },
        ),
        # Test Case 3: Get min temperature for sensors 1 and 2 for the last day
        (
            [1, 2],
            [schemas.Metric.TEMPERATURE],
            [schemas.Statistic.MIN],
            timedelta(days=1),
            {"temperature_min": 0.0},
        ),
    ],
)
@freeze_time("2020-01-10")
async def test_get_sensor_data_statistics_valid_input(
    data_prepared_db,
    db_session,
    sensors,
    metrics,
    statistics,
    time_period,
    expected_output,
):
    """
    Test that various inputs are producing the right quesy results.
    """
    stats = await data_access.get_sensor_data_statistics(
        db_session, sensors, metrics, statistics, time_period
    )
    assert stats.keys() == expected_output.keys()
    for key, expected_value in expected_output.items():
        assert stats[key] == pytest.approx(expected_value, abs=0.01)
