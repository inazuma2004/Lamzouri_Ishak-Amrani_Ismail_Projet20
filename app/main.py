"""API REST pour la classification automatique d'incidents IT.
"""
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.model import load_model
from app.schemas import (
    HealthResponse,
    PredictRequest,
    PredictResponse,
    ResolveRequest,
    ResolveResponse,
)
from app.securite import exiger, identifier
from incidents_app.agent import IncidentAgent
from incidents_app.rag import MiniRAG

load_dotenv()  # lit .env s'il existe ; ne remplace jamais une variable déjà définie
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("incident_api")

CODES = {400: "REQUETE_INVALIDE", 401: "NON_AUTHENTIFIE", 403: "ACCES_REFUSE", 404: "INTROUVABLE",
         405: "METHODE_NON_AUTORISEE", 422: "ENTREE_INVALIDE", 500: "ERREUR_INTERNE",
         503: "MODELE_INDISPONIBLE"}


def _erreur(statut: int, message: str, en_tetes: dict[str, str] | None = None) -> JSONResponse:
    corps = {"erreur": {"code": CODES.get(statut, f"HTTP_{statut}"), "message": message}}
    return JSONResponse(corps, status_code=statut, headers=en_tetes)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de l'API Incidents IT...")
    nb_cles = 0
    try:
        from app.securite import charger_cles
        nb_cles = len(charger_cles())
    except ValueError as e:
        logger.warning("Clés d'API mal configurées (%s) : les routes protégées répondront 401/403", e)
    if nb_cles == 0:
        logger.warning("Aucune clé dans API_KEYS : les routes /predict et /resolve répondront 401")
    app.state.classifier = load_model()
    agent = IncidentAgent(rag=MiniRAG())
    # Prépare la base vectorielle pour que le premier /resolve soit immédiat.
    agent.rag.charger_ou_indexer()
    app.state.agent = agent
    logger.info("Modèle chargé ; %d clé(s) d'API", nb_cles)
    yield
    logger.info("Arrêt de l'API")

app = FastAPI(
    title="Incident Classification API",
    description="API de routage intelligent pour tickets d'assistance IT.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # la clé passe dans un en-tête, pas dans un cookie
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)


@app.exception_handler(StarletteHTTPException)
async def erreur_http(request: Request, exc: StarletteHTTPException) -> Response:
    if isinstance(exc.detail, dict) and exc.detail.get("code"):
        return _erreur(exc.status_code, str(exc.detail), en_tetes=getattr(exc, "headers", None))
    if request.url.path in {"/predict", "/resolve"}:
        return _erreur(exc.status_code, str(exc.detail), en_tetes=getattr(exc, "headers", None))
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def erreur_validation(request: Request, exc: RequestValidationError) -> Response:
    if request.url.path in {"/predict", "/resolve"}:
        corps = {"erreur": {"code": "ENTREE_INVALIDE",
                            "message": "Entrée refusée par le contrat de l'API",
                            "champs": [{"champ": ".".join(str(x) for x in e["loc"]),
                                        "message": e["msg"]} for e in exc.errors()]}}
        return JSONResponse(corps, status_code=422)
    return await request_validation_exception_handler(request, exc)


def _classifier():
    if not hasattr(app.state, "classifier"):
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return app.state.classifier

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Point de santé public (interrogé par Docker), sans clé d'API."""
    return {"status": "OK", "model": _classifier().model_name}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest, role: str = Depends(exiger("client"))):
    try:
        result = _classifier().predict(request.text)
        result["text"] = request.text
        logger.info("predict: %r -> %s (%.2f) par %s", request.text[:50], result["label"], result["score"], role)
        return result
    except Exception as e:
        logger.exception("Erreur de prédiction")
        raise HTTPException(status_code=500, detail=str(e))


def _agent() -> IncidentAgent:
    if not hasattr(app.state, "agent"):
        raise HTTPException(status_code=503, detail="Agent non initialisé")
    return app.state.agent


@app.post("/resolve", response_model=ResolveResponse)
async def resolve(request: ResolveRequest, role: str = Depends(exiger("client"))):
    """Résolution d'incident par l'agent autonome (ML + RAG).

    - 200 : résolution retournée avec catégorie, procédure RAG et sources citées
    - 401 : clé d'API manquante ou invalide
    - 403 : rôle insuffisant
    - 422 : texte vide ou trop long (Pydantic standard)
    - 503 : agent non initialisé
    - 500 : erreur interne
    """
    try:
        resultat = _agent().resoudre(request.text)
        logger.info("resolve: %r -> %s (%s) par %s", request.text[:50], resultat["categorie"], resultat["statut"], role)
        return resultat
    except Exception as e:
        logger.exception("Erreur de résolution agentique")
        raise HTTPException(status_code=500, detail=str(e)) from None
