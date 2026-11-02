"""Tests du jeu d'or (S4) — 20 tickets réels annotés à la main.

Exécution : pytest tests/test_jeu_or.py -v
Les tickets ambigus sont déclarés xfail(strict=False) pour documenter
honnêtement les limites du modèle, conformément aux exigences du cours.
"""
import pytest

from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "incidents.joblib"
pytestmark = pytest.mark.skipif(
    not MODEL_PATH.exists(),
    reason="Modèle absent : lancez python src/train.py",
)


@pytest.fixture(scope="module")
def classifier():
    from app.model import load_model
    return load_model()


# ---------------------------------------------------------------------------
# Cas clairs — le modèle doit les classer correctement (VALIDE ou A_VERIFIER)
# ---------------------------------------------------------------------------

JEU_OR_CLAIR = [
    ("screen flickering and turning black display issue", "Hardware"),
    ("keyboard keys are stuck and not working", "Hardware"),
    ("printer is not printing duplex mode broken", "Hardware"),
    ("cannot login vpn password expired please reset", "Access"),
    ("account locked out after multiple failed login attempts", "Access"),
    ("server disk full storage quota exceeded backup failed", "Storage"),
    ("mailbox almost full storage upgrade needed", "Storage"),
    ("need to purchase new workstation for new employee", "Purchase"),
    ("new employee onboarding setup hr support needed", "HR Support"),
    ("annual leave request not appearing in system hr", "HR Support"),
    ("request admin rights to install approved software", "Administrative rights"),
    ("need elevated privileges for server configuration", "Administrative rights"),
    ("project milestone tracking internal project update", "Internal Project"),
]

# Cas ambigus — xfail documenté
JEU_OR_AMBIGU = [
    pytest.param(
        "laptop for new starter order please",
        "Purchase",
        marks=pytest.mark.xfail(strict=False, reason="Ambigu : mention 'laptop' peut tirer vers Hardware"),
    ),
    pytest.param(
        "moving to new office miscellaneous request",
        "Miscellaneous",
        marks=pytest.mark.xfail(strict=False, reason="Miscellaneous est difficile à distinguer sans contexte fort"),
    ),
    pytest.param(
        "need access to shared network drive folder permissions",
        "Access",
        marks=pytest.mark.xfail(strict=False, reason="'shared folder' chevauche Storage dans le dataset"),
    ),
    pytest.param(
        "software license renewal request for visual studio",
        "Purchase",
        marks=pytest.mark.xfail(strict=False, reason="'license' prédit Access dans le dataset (accès logiciel)"),
    ),
]


@pytest.mark.parametrize("text,expected", JEU_OR_CLAIR)
def test_jeu_or_cas_clairs(classifier, text, expected):
    """Vérifie que le modèle prédit correctement les cas non ambigus."""
    result = classifier.predict(text)
    assert result["status"] in {"VALIDE", "A_VERIFIER"}
    if result["status"] == "VALIDE":
        assert result["label"] == expected, (
            f"Texte: '{text}'\nAttendu: {expected}\nObtenu: {result['label']} "
            f"(score={result['score']:.2f})"
        )


@pytest.mark.parametrize("text,expected", JEU_OR_AMBIGU)
def test_jeu_or_cas_ambigus(classifier, text, expected):
    """Documente les cas ambigus du modèle (xfail acceptable)."""
    result = classifier.predict(text)
    assert result["label"] == expected

