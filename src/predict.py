"""Chargement et prédiction du modèle d'incidents IT.

Le modèle est cherché dans cet ordre :
1. la variable d'environnement INCIDENT_MODELE, si elle est definie ;
2. models/incidents.joblib a la racine du depot (usage depuis les sources).

Dans une roue installee hors du depot, il faut donc fournir INCIDENT_MODELE.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import joblib

# Variable d'environnement pour decouplage modele/code (standard TP6)
ENV_MODELE = "INCIDENT_MODELE"

# Seuil d'abstention : sous ce score, le modele ne tranche pas.
SEUIL_ABSTENTION = 0.60


class ModeleIntrouvable(FileNotFoundError):
    """Levee quand le fichier du modele n'existe pas a l'endroit attendu."""


def chemin_modele() -> Path:
    """Renvoie le chemin du modele selon la variable d'environnement ou le depot."""
    env = os.environ.get(ENV_MODELE)
    if env:
        return Path(env)
    racine = Path(__file__).resolve().parents[1]
    return racine / "models" / "incidents.joblib"


def _nettoyer_texte(texte: str) -> str:
    if not isinstance(texte, str):
        raise TypeError("texte doit etre une chaine de caracteres")
    t = texte.strip()
    if not t:
        raise ValueError("texte vide")
    return t


def charger_modele(chemin: Path | None = None):
    """Charge le pipeline scikit-learn sauvegarde au TP2."""
    chemin = Path(chemin) if chemin is not None else chemin_modele()
    if not chemin.exists():
        raise ModeleIntrouvable(
            f"modele introuvable : {chemin}. "
            f"Definissez {ENV_MODELE} ou lancez python src/train.py dans le depot."
        )
    return joblib.load(chemin)


def predire(texte: str, modele=None, seuil: float = SEUIL_ABSTENTION) -> dict[str, Any]:
    """Renvoie {'label': str, 'score': float, 'status': str}.

    status vaut 'VALIDE' si score >= seuil, sinon 'A_VERIFIER'.
    """
    if modele is None:
        modele = charger_modele()
    t = _nettoyer_texte(texte)
    proba = modele.predict_proba([t])[0]
    idx = int(proba.argmax())
    score = float(proba[idx])
    if score < seuil:
        return {"label": "INDETERMINE", "score": round(score, 4), "status": "A_VERIFIER"}
    label = str(modele.classes_[idx])
    return {"label": label, "score": round(score, 4), "status": "VALIDE"}


# Alias retrocompatible pour les tests existants
def predict(texte: str, *, modele=None, modele_path=None, seuil: float = 0.0) -> dict[str, Any]:
    if modele is None and modele_path is not None:
        modele = charger_modele(chemin=Path(modele_path))
    return predire(texte, modele=modele, seuil=seuil)


def main() -> int:
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    texte = " ".join(sys.argv[1:])
    try:
        res = predire(texte)
    except ModeleIntrouvable as e:
        print(f"Erreur : {e}")
        return 1
    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
