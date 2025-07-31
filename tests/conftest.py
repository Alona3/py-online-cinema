import pytest
from fastapi.testclient import TestClient
from app.main import app  # твій FastAPI додаток

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
