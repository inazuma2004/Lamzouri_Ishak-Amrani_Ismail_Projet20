"""Chargement du modèle et prédiction, sans aucun chemin codé en dur vers le dépôt.

Le modèle est cherché dans cet ordre :
1. la variable d'environnement INCIDENTS_MODELE, si elle est définie ;
2. models/incidents.joblib à la racine du dépôt, quand le paquet est utilisé depuis les sources.

Dans une roue installée hors du dépôt, il faut donc fournir INCIDENTS_MODELE.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import joblib

# Seuil d'abstention : sous ce score, le modèle ne tranche pas.
# Aligné sur la valeur retenue au TP4 (courbe_seuil.py).
SEUIL_ABSTENTION = 0.60
ENV_MODELE = "INCIDENTS_MODELE"


class ModeleIntrouvable(FileNotFoundError):
    """Levée quand le fichier du modèle n'existe pas à l'endroit attendu."""


def chemin_modele() -> Path:
    """Renvoie le chemin du modèle selon la variable d'environnement ou le dépôt.

    Dans une roue installée, le modèle est embarqué dans le paquet
    (incidents_app/models/incidents.joblib). Depuis les sources du dépôt,
    il se trouve à la racine (models/incidents.joblib).
    """
    env = os.environ.get(ENV_MODELE)
    if env:
        return Path(env)
    # 1. Modèle embarqué dans le paquet (roue installée)
    paquet_modele = Path(__file__).resolve().parent / "models" / "incidents.joblib"
    if paquet_modele.exists():
        return paquet_modele
    # 2. Modèle à la racine du dépôt (utilisation depuis les sources)
    racine = Path(__file__).resolve().parents[1]
    return racine / "models" / "incidents.joblib"


def _nettoyer_texte(texte: str) -> str:
    if not isinstance(texte, str):
        raise TypeError("texte doit être une chaîne de caractères")
    t = texte.strip()
    if not t:
        raise ValueError("texte vide")
    return t


def charger_modele(chemin: Path | None = None):
    """Charge le pipeline scikit-learn sauvegardé."""
    chemin = Path(chemin) if chemin is not None else chemin_modele()
    if not chemin.exists():
        raise ModeleIntrouvable(
            f"modèle introuvable : {chemin}. Définissez {ENV_MODELE} "
            "ou lancez python src/train.py dans le dépôt."
        )
    return joblib.load(chemin)


def predire(texte: str, modele=None, seuil: float = SEUIL_ABSTENTION) -> dict[str, Any]:
    """Renvoie {'label': ..., 'score': ..., 'status': ...} avec abstention sous SEUIL_ABSTENTION.

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


# Alias rétrocompatible pour les tests existants (src.predict.predict)
def predict(texte: str, *, modele=None, modele_path=None, seuil: float = 0.0) -> dict[str, Any]:
    if modele is None and modele_path is not None:
        from pathlib import Path as _P

        modele = charger_modele(chemin=_P(modele_path))
    if seuil == 0.0:
        seuil = SEUIL_ABSTENTION
    return predire(texte, modele=modele, seuil=seuil)


def main() -> int:
    import json
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
