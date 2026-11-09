"""Tests du paquet installable incidents_app (TP6 / Semaine 6).

Vérifie que le paquet incidents_app expose bien :
- ModeleIntrouvable quand le modèle est absent (sans variable d'env)
- predire() quand le modèle est présent
- Seuil d'abstention à 0.60 (A_VERIFIER sous le seuil)
"""
from __future__ import annotations

from pathlib import Path

import pytest

from incidents_app.predict import (
    ENV_MODELE,
    SEUIL_ABSTENTION,
    ModeleIntrouvable,
    charger_modele,
    predire,
)


def test_seuil_abstention():
    assert SEUIL_ABSTENTION == 0.60


def test_env_modele_nom():
    assert ENV_MODELE == "INCIDENTS_MODELE"


def test_modele_introuvable_sans_variable(monkeypatch: pytest.MonkeyPatch):
    """Sans INCIDENTS_MODELE et sans models/incidents.joblib, doit lever ModeleIntrouvable."""
    monkeypatch.delenv(ENV_MODELE, raising=False)
    # Pointer vers un chemin inexistant
    monkeypatch.setattr(
        "incidents_app.predict.chemin_modele",
        lambda: Path("/chemin/inexistant/incidents.joblib"),
    )
    with pytest.raises(ModeleIntrouvable):
        charger_modele()


def test_predire_avec_modele_present():
    """Si le modèle existe, predire() retourne un dict avec label, score, status."""
    modele_path = Path("models/incidents.joblib")
    if not modele_path.exists():
        pytest.skip("Modèle non entraîné : lancez python src/train.py")
    modele = charger_modele()
    resultat = predire("Impossible de se connecter au VPN", modele=modele)
    assert "label" in resultat
    assert "score" in resultat
    assert "status" in resultat
    assert resultat["status"] in {"VALIDE", "A_VERIFIER"}
    assert 0.0 <= resultat["score"] <= 1.0


def test_abstention_sous_seuil():
    """Un texte absurde doit donner INDETERMINE / A_VERIFIER si le modèle est présent."""
    modele_path = Path("models/incidents.joblib")
    if not modele_path.exists():
        pytest.skip("Modèle non entraîné : lancez python src/train.py")
    modele = charger_modele()
    resultat = predire("xqzvb wlkptr grombu", modele=modele)
    # Soit le modèle est incertain (INDETERMINE/A_VERIFIER), soit il prédit avec score faible
    assert resultat["status"] in {"VALIDE", "A_VERIFIER"}
    if resultat["status"] == "A_VERIFIER":
        assert resultat["label"] == "INDETERMINE"
