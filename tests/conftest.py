"""
Contains pytest fixtures for unit tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    """
    Fixture that provides a test client for the FastAPI app.
    """
    with TestClient(app) as c:
        yield c
