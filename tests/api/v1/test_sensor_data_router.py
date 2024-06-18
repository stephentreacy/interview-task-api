"""
Contains tests for the /sensor-data endpoint of the application.

"""

import pytest
from fastapi import status


def test_add_sensor_data_success(client, sensor_data_payload):
    """
    Test sent data is added successfully and returned.
    """
    response = client.post("/api/v1/sensor-data", json=sensor_data_payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == sensor_data_payload


@pytest.mark.parametrize(
    "field_to_invalidate, invalid_value",
    [
        ("sensor_id", None),
        ("sensor_id", -1),
        ("sensor_id", "str"),
        ("timestamp", None),
        ("timestamp", "str"),
        ("temperature", None),
        ("temperature", "str"),
        ("humidity", None),
        ("humidity", -1),
        ("humidity", "str"),
        ("wind_speed", None),
        ("wind_speed", -1),
        ("wind_speed", "str"),
    ],
)
def test_add_sensor_data_with_invalid_field(
    client,
    sensor_data_payload,
    field_to_invalidate,
    invalid_value,
):
    """
    Test that invalid data is blocked by FastAPI.
    """
    sensor_data_payload[field_to_invalidate] = invalid_value

    response = client.post("/api/v1/sensor-data", json=sensor_data_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_sensor_data_server_error(client, mocker, sensor_data_payload):
    """
    Test that a server error is returned if the database operation fails.
    """
    mocker.patch(
        "app.data_access.create_sensor_data", side_effect=Exception("Database error")
    )
    response = client.post("/api/v1/sensor-data", json=sensor_data_payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
