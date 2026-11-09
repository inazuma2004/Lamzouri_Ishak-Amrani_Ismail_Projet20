# Journal des versions — incidents-app

## [1.0.0] — 2026-11-09

### Ajouté
- Paquet Python redistribuable `incidents-app` (roue + sdist), version 1.0.0
- Commande CLI `incidents` (predict, serve, --version)
- Modèle ML embarqué dans la roue : `incidents_app/models/incidents.joblib`
- Sécurisation de l'API par clé d'API (en-tête `X-API-Key`, rôles client/admin)
- Traitement par lot CSV dans l'interface Streamlit (3e onglet)
- Mini-RAG extractif local : 8 runbooks, ChromaDB, sentence-transformers (S9-S10)
- Agent autonome de résolution (ML → RAG, seuil d'incertitude 0,60)
- Tests unitaires et d'intégration (pytest), lint (ruff), typage (mypy)
- Dockerisation (Dockerfile, docker-compose.yml)

### Modifié
- Version du paquet passée de 0.6.0 à 1.0.0
- `__version__` du paquet `incidents_app` passé à 1.0.0
