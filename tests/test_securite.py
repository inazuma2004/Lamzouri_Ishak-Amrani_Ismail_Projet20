"""Tests de sécurisation de l'API par clé d'API (TP 2).

- /health reste public (sans clé).
- /predict et /resolve exigent l'en-tête X-API-Key (401 sinon).
- Une bonne clé client renvoie 200.
- Une mauvaise clé renvoie 401.
"""
import os

import pytest
from fastapi.testclient import TestClient

CLE_CLIENT = "cle-client-des-tests-unitaires"
CLE_ADMIN = "cle-admin-des-tests-unitaires"


@pytest.fixture(scope="module")
def client():
    """TestClient avec deux clés configurées dans l'environnement."""
    precedent = os.environ.get("API_KEYS")
    os.environ["API_KEYS"] = f"{CLE_CLIENT}:client,{CLE_ADMIN}:admin"
    from app.main import app
    with TestClient(app) as c:
        yield c
    if precedent is None:
        os.environ.pop("API_KEYS", None)
    else:
        os.environ["API_KEYS"] = precedent


def test_health_public_sans_cle(client):
    """Le point de santé est accessible sans clé d'API."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "OK"


def test_predict_sans_cle_401(client):
    """Sans en-tête X-API-Key, /predict refuse avec 401."""
    r = client.post("/predict", json={"text": "Cannot access the VPN"})
    assert r.status_code == 401
    assert "WWW-Authenticate" in r.headers


def test_predict_mauvaise_cle_401(client):
    """Une clé inconnue sur /predict renvoie 401."""
    r = client.post("/predict", json={"text": "Cannot access the VPN"},
                    headers={"X-API-Key": "cle-inconnue"})
    assert r.status_code == 401


def test_predict_bonne_cle_200(client):
    """Avec une clé client valide, /predict renvoie 200."""
    r = client.post("/predict", json={"text": "Cannot access the VPN"},
                    headers={"X-API-Key": CLE_CLIENT})
    assert r.status_code == 200
    body = r.json()
    assert "label" in body and "score" in body and "status" in body


def test_resolve_sans_cle_401(client):
    """Sans en-tête X-API-Key, /resolve refuse avec 401."""
    r = client.post("/resolve", json={"text": "Cannot access the VPN"})
    assert r.status_code == 401


def test_resolve_bonne_cle_200(client):
    """Avec une clé client valide, /resolve renvoie 200."""
    r = client.post("/resolve", json={"text": "Cannot access the VPN"},
                    headers={"X-API-Key": CLE_CLIENT})
    assert r.status_code == 200
    body = r.json()
    assert "categorie" in body and "statut" in body


def test_predict_texte_vide_422_meme_avec_cle(client):
    """Même authentifié, un texte vide est refusé en 422."""
    r = client.post("/predict", json={"text": ""},
                    headers={"X-API-Key": CLE_CLIENT})
    assert r.status_code == 422
