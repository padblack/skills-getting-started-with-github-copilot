import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity database before each test."""
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)


@pytest.fixture
def client():
    return TestClient(app_module.app)
