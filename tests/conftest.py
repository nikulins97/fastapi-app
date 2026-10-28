import pytest
from fastapi.testclient import TestClient

from main import app
import repository


@pytest.fixture(autouse=True)
def clean_storage():
    repository.analyses.clear()
    repository.next_id = 1
    yield
    repository.analyses.clear()
    repository.next_id = 1


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def created(client):
    response = client.post("/analyses", json={"name": "test", "image_url": "https://www.google.com/"})
    return response.json()