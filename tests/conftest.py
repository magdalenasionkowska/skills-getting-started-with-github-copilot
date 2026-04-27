import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset participants list before each test to ensure isolation."""
    original_participants = {
        name: list(data["participants"]) for name, data in activities.items()
    }
    yield
    for name, data in activities.items():
        data["participants"] = original_participants[name]
