# Dockerfile — Semaine 6 : Dockerisation & Déploiement
# Image de production pour l'API de classification d'incidents IT.
FROM python:3.11-slim

WORKDIR /app

# Dépendances Python (figées pour reproductibilité)
COPY requirements.txt .
# PyTorch CPU uniquement : image légère, portable, sans GPU ni paquets CUDA
RUN pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        --extra-index-url https://pypi.org/simple \
        torch \
    && pip install --no-cache-dir -r requirements.txt

# Code de l'application (sauf artefacts exclus par .dockerignore)
COPY . .

# Mini-RAG (S9) : pré-télécharger le modèle d'embedding et construire l'index
# des runbooks dans l'image, pour que /resolve fonctionne dès le démarrage.
RUN python -m incidents_app.rag --indexer

# Port exposé par l'API FastAPI
EXPOSE 8000

# Variable d'environnement du modèle (à surcharger à l'exécution si besoin)
# INCIDENTS_MODELE=/app/models/incidents.joblib

# Lancement de l'API avec uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
