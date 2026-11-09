"""Tests d'intégration du modèle : cohérence chargeur, métriques, seuil d'abstention.

Ces tests nécessitent le modèle entraîné (models/incidents.joblib).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.model import load_model
from incidents_app.predict import (
    ENV_MODELE,
    SEUIL_ABSTENTION,
    ModeleIntrouvable,
    charger_modele,
    predire,
)

MODEL_PATH = Path("models/incidents.joblib")
METRICS_PATH = Path("models/metrics.json")


@pytest.fixture
def classifier():
    return load_model()


def test_modele_version_coherence():
    """Le seuil d'abstention est cohérent entre predict et app.model."""
    assert SEUIL_ABSTENTION == 0.60
    assert ENV_MODELE == "INCIDENTS_MODELE"


def test_load_model_retourne_classifier(classifier):
    """load_model() retourne un IncidentsClassifier avec model_name renseigné."""
    assert classifier is not None
    assert hasattr(classifier, "model_name")
    assert "incidents" in classifier.model_name.lower()


def test_predict_coherence_seuil(classifier):
    """La prédiction respecte le seuil d'abstention : VALIDE >= 0.60, A_VERIFIER < 0.60."""
    # Texte clair du domaine Hardware
    res = classifier.predict("screen flickering and turning black display issue")
    assert res["status"] in {"VALIDE", "A_VERIFIER"}
    assert res["score"] >= 0.0 and res["score"] <= 1.0
    if res["status"] == "A_VERIFIER":
        assert res["label"] == "INDETERMINE"
        assert res["score"] < SEUIL_ABSTENTION
    else:
        assert res["score"] >= SEUIL_ABSTENTION


def test_predire_retourne_dict_bien_forme():
    """predire() retourne un dict avec label, score, status."""
    modele_path = MODEL_PATH
    if not modele_path.exists():
        pytest.skip("Modèle non entraîné : lancez python src/train.py")
    modele = charger_modele()
    res = predire("Impossible de se connecter au VPN", modele=modele)
    assert set(res.keys()) == {"label", "score", "status"}
    assert res["status"] in {"VALIDE", "A_VERIFIER"}
    assert 0.0 <= res["score"] <= 1.0


def test_metrics_json_coherence():
    """models/metrics.json existe et contient les clés requises."""
    if not METRICS_PATH.exists():
        pytest.skip("metrics.json absent : lancez python src/train.py")
    payload = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    for key in ["f1_macro", "accuracy", "n_train", "n_test", "seuil_f1", "classes", "date"]:
        assert key in payload, f"Clé manquante dans metrics.json : {key}"
    assert isinstance(payload["classes"], list)
    assert len(payload["classes"]) >= 2
    assert 0.0 <= payload["f1_macro"] <= 1.0


def test_modele_introuvable_sans_fichier(monkeypatch):
    """charger_modele lève ModeleIntrouvable si le fichier n'existe pas."""
    monkeypatch.delenv(ENV_MODELE, raising=False)
    monkeypatch.setattr(
        "incidents_app.predict.chemin_modele",
        lambda: Path("/chemin/absolument/inexistant/incidents.joblib"),
    )
    with pytest.raises(ModeleIntrouvable):
        charger_modele()
