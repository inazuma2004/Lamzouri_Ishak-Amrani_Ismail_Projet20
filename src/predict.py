"""Wrapper rétrocompatible : délègue à incidents_app.predict (source de vérité).

Les tests existants qui font ``from src.predict import predict`` continuent de fonctionner.
"""

from __future__ import annotations

from incidents_app.predict import (
    ENV_MODELE,
    SEUIL_ABSTENTION,
    ModeleIntrouvable,
    charger_modele,
    chemin_modele,
    predire,
)

__all__ = [
    "ENV_MODELE",
    "SEUIL_ABSTENTION",
    "ModeleIntrouvable",
    "charger_modele",
    "chemin_modele",
    "predict",
    "predire",
]


def predict(texte: str, *, modele=None, modele_path=None, seuil: float = 0.0) -> dict:
    """Alias rétrocompatible pour les tests existants (test_week2_train.py)."""
    if modele is None and modele_path is not None:
        from pathlib import Path as _P

        modele = charger_modele(chemin=_P(modele_path))
    if seuil == 0.0:
        seuil = SEUIL_ABSTENTION
    return predire(texte, modele=modele, seuil=seuil)
