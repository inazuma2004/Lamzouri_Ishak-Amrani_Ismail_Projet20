
import os
from dataclasses import dataclass

import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

@dataclass
class Reponse:
    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""

def creer_session() -> httpx.Client:
    return httpx.Client(base_url=API_URL, timeout=10)

def predire(session: httpx.Client, texte: str) -> Reponse:
    try:
        r = session.post("/predict", json={"text": texte})
        if r.status_code == 200:
            data = r.json()
            return Reponse(True, label=data["label"], score=data["score"])
        return Reponse(False, message=f"Erreur API ({r.status_code})")
    except httpx.RequestError:
        return Reponse(False, message="API injoignable")
