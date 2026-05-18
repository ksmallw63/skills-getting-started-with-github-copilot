import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app

original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def restore_activities():
    yield
    app_module.activities = copy.deepcopy(original_activities)


@pytest.fixture
def client():
    return TestClient(app)
