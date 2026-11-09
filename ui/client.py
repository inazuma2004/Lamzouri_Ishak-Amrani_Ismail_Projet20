"""Client HTTP de l'API (TP 3) : tout ce que l'interface sait de l'API passe par ce module.

L'interface n'importe jamais predict() ni le fichier .joblib : elle appelle l'API
avec la clé lue dans API_KEY (fichier .env), et traduit chaque réponse en message lisible.
"""
import os
from collections import Counter
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

load_dotenv()  # Streamlit ne lit pas .env de lui-même ; une variable déjà définie n'est pas remplacée
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
API_KEY = os.environ.get("API_KEY", "")

INJOIGNABLE = "API injoignable : lancez d'abord uvicorn app.main:app"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
SANS_MODELE = "Modèle non chargé : relancer l'API après avoir produit le modèle."
CLE = "Clé d'API absente, invalide ou sans droit : vérifiez API_KEY dans le fichier .env."


@dataclass
class Reponse:
    """Ce que l'interface affiche : un verdict, ou un message d'erreur lisible."""

    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""
    statut: str | None = None
    runbook: str | None = None
    resolution: str | None = None
    sources: list | None = None
    action_humaine: bool | None = None
    message_humain: str | None = None


def creer_session() -> httpx.Client:
    """La connexion à l'API, avec la clé d'API dans l'en-tête X-API-Key."""
    return httpx.Client(base_url=API_URL, timeout=10, headers={"X-API-Key": API_KEY})


def _code(r: httpx.Response) -> str:
    """Le code stable d'une erreur (NON_AUTHENTIFIE, ACCES_REFUSE...), ou une chaîne vide."""
    try:
        return r.json()["erreur"]["code"]
    except (ValueError, KeyError, TypeError):
        return ""


def _traiter_erreur(r: httpx.Response) -> Reponse:
    code = _code(r)
    if r.status_code == 401 or code == "NON_AUTHENTIFIE":
        return Reponse(False, message=CLE)
    if r.status_code == 403 or code == "ACCES_REFUSE":
        return Reponse(False, message=CLE)
    if r.status_code == 422 or code == "ENTREE_INVALIDE":
        return Reponse(False, message=REFUS)
    if r.status_code == 503 or code == "MODELE_INDISPONIBLE":
        return Reponse(False, message=SANS_MODELE)
    return Reponse(False, message=f"Erreur interne de l'API ({r.status_code}).")


def predire(session: httpx.Client, texte: str) -> Reponse:
    try:
        r = session.post("/predict", json={"text": texte})
    except httpx.RequestError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        data = r.json()
        return Reponse(
            True,
            label=data["label"],
            score=data["score"],
            statut=data.get("status"),
            message=data.get("label", ""),
        )
    return _traiter_erreur(r)


def resoudre(session: httpx.Client, texte: str) -> Reponse:
    """Appelle l'endpoint /resolve de l'agent autonome (ML + RAG)."""
    try:
        r = session.post("/resolve", json={"text": texte})
    except httpx.RequestError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        data = r.json()
        return Reponse(
            True,
            label=data.get("categorie"),
            score=data.get("score"),
            statut=data.get("statut"),
            runbook=data.get("runbook"),
            resolution=data.get("resolution"),
            sources=data.get("sources", []),
            action_humaine=data.get("action_humaine"),
            message_humain=data.get("message_humain"),
            message=data.get("categorie", ""),
        )
    return _traiter_erreur(r)


def predire_lot(session: httpx.Client, textes: list[str]) -> list[Reponse]:
    return [predire(session, texte) for texte in textes]


def resumer(reponses: list[Reponse]) -> dict[str, int]:
    """Nombre de tickets par catégorie/statut ; les refus et erreurs sont comptés à part."""
    compte: Counter[str] = Counter()
    for r in reponses:
        if r.ok:
            compte[f"{r.label} ({r.statut})"] += 1
        else:
            compte["REFUS OU ERREUR"] += 1
    return dict(sorted(compte.items()))
