
import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

CLE_TEST = "cle-client-des-tests-limites"


@pytest.fixture
def client():
    precedent = os.environ.get("API_KEYS")
    os.environ["API_KEYS"] = f"{CLE_TEST}:client"
    with TestClient(app, headers={"X-API-Key": CLE_TEST}) as c:
        yield c
    if precedent is None:
        os.environ.pop("API_KEYS", None)
    else:
        os.environ["API_KEYS"] = precedent


def test_texte_trop_long_422(client):
    # Dépasse 2000 caractères
    response = client.post("/predict", json={"text": "a" * 2001})
    assert response.status_code == 422

def test_texte_vide_422(client):
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422
