import pytest
from copy import deepcopy
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    # Arrange: snapshot original in-memory activities so tests can modify safely
    original_activities = deepcopy(app_module.activities)
    try:
        # Act: provide a TestClient for the FastAPI app
        with TestClient(app_module.app) as test_client:
            yield test_client
    finally:
        # Assert/Teardown: restore original activities to avoid test cross-talk
        app_module.activities.clear()
        app_module.activities.update(original_activities)
