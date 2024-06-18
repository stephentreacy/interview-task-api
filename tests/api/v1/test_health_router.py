"""
Contains tests for the health endpoint of the application.

"""

from fastapi import status


def test_health_endpoint(client):
    """
    Test basic health check.
    """
    response = client.get("api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
