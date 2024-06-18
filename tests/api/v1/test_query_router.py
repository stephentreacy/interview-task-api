from datetime import timedelta
from unittest.mock import ANY, AsyncMock

import pytest
from fastapi import status

from app.schemas import Metric, Statistic

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "query_string,expected_params",
    [
        ("", [None, [*Metric], [*Statistic], timedelta(days=1)]),
        ("?sensors=1&sensors=2", [[1, 2], [*Metric], [*Statistic], timedelta(days=1)]),
        (
            "?metrics=temperature&metrics=humidity",
            [
                None,
                [Metric.TEMPERATURE, Metric.HUMIDITY],
                [*Statistic],
                timedelta(days=1),
            ],
        ),
        ("?statistics=min", [None, [*Metric], [Statistic.MIN], timedelta(days=1)]),
        ("?time_period=P7D", [None, [*Metric], [*Statistic], timedelta(days=7)]),
    ],
)
async def test_query_sensor_data_params(client, mocker, query_string, expected_params):
    """
    Test that the query parameters are correctly parsed and passed to the data access function.
    """
    mock_get_stats = mocker.patch(
        "app.api.v1.endpoints.query.get_sensor_data_statistics",
        new_callable=AsyncMock,
        return_value={"temperature_avg": 20.0},
    )

    response = client.get(f"/api/v1/query/{query_string}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"temperature_avg": 20.0}
    mock_get_stats.assert_called_once_with(
        ANY, *expected_params
    )  # ANY for the db session


async def test_query_server_error(client, mocker):
    """
    Test that a server error is returned if the database operation fails.
    """
    mocker.patch(
        "app.api.v1.endpoints.query.get_sensor_data_statistics",
        new_callable=AsyncMock,
        side_effect=Exception("Database error"),
    )
    response = client.get("/api/v1/query")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
