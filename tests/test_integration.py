"""Tests d'intégration de l'API (S3/S4) — le modèle doit être entraîné au préalable."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

MODELE = pytest.importorskip  # garde-fou : skip si modèle absent
from pathlib import Path  # noqa: E402

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "incidents.joblib"
pytestmark = pytest.mark.skipif(
    not MODEL_PATH.exists(),
    reason="Modèle absent : lancez python src/train.py",
)


@pytest.fixture(scope="module")
def client():
    """Le 'with' déclenche le lifespan : le modèle est chargé une fois."""
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert "model" in response.json()


def test_predict_endpoint(client):
    response = client.post("/predict", json={"text": "Network connection error"})
    assert response.status_code == 200
    body = response.json()
    assert "label" in body
    assert "score" in body
    assert body["status"] in {"VALIDE", "A_VERIFIER"}


def test_predict_texte_vide_422(client):
    assert client.post("/predict", json={"text": ""}).status_code == 422
    assert client.post("/predict", json={"text": "   "}).status_code == 422


def test_predict_champ_manquant_422(client):
    assert client.post("/predict", json={}).status_code == 422

