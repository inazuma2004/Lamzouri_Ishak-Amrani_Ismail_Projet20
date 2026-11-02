"""API REST pour la classification automatique d'incidents IT.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.model import load_model
from app.schemas import HealthResponse, PredictRequest, PredictResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("incident_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de l'API Incidents IT...")
    app.state.classifier = load_model()
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _classifier():
    if not hasattr(app.state, "classifier"):
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return app.state.classifier

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "OK", "model": _classifier().model_name}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        result = _classifier().predict(request.text)
        result["text"] = request.text
        return result
    except Exception as e:
        logger.exception("Erreur de prédiction")
        raise HTTPException(status_code=500, detail=str(e))
