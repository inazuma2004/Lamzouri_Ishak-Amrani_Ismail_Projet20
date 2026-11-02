
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_texte_trop_long_422(client):
    # Dépasse 2000 caractères
    response = client.post("/predict", json={"text": "a" * 2001})
    assert response.status_code == 422

def test_texte_vide_422(client):
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422
