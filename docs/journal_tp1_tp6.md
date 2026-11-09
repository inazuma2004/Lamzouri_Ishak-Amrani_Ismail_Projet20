# 📓 Journal de bord — Projet Agent Autonome de Résolution d'Incidents IT

> **Projet :** incidentsIT (IT Helpdesk Intelligent)  
> **Module :** Développement et déploiement d'applications intelligentes (2026-2027)  
> **Enseignant :** M. A. Larhlimi  
> **Binôme :** Ishak Lamzouri (Membre A) & Ismail Amrani (Membre B)  
> **Dépôt :** `projet_incidentsIT`  
> **Architecture appliquée :** conforme aux phases du cours (Atelier 0 → TP1 → TP2 → TP3 → TP4 → projet 4 semaines), propre au domaine IT Incidents

---

## 🗺️ Légende des points de contrôle

| Symbole | Signification |
|---------|---------------|
| ✅ | Réalisé et vérifié |
| ⏳ | En cours |
| ⬜ | À venir (semaine suivante) |

---

## Semaine 1 — TP1 : Cadrage & environnement

- [x] **T0** Structure de dépôt initialisée (`src/`, `app/`, `ui/`, `tests/`, `models/`, `data/`, `docs/`, `scripts/`)
- [x] **T1** `.gitignore` strict : exclusion de `.venv/`, `*.joblib`, `*.csv`, `dist/`, `build/`, `*.egg-info/`
- [x] **T2** `pyproject.toml` : packaging PEP 621, nom `incidents-app`, version `0.6.0`, entry point `incidents = "incidents_app.cli:main"`
- [x] **T3** `requirements.txt` : versions épinglées pour reproductibilité (scikit-learn 1.9.1, pandas 3.1.1, fastapi, streamlit, pytest, ruff)
- [x] **T4** `scripts/check_setup.py` : diagnostic de l'environnement (0 erreur)
- [x] **T5** `pytest` configuré (`pythonpath = ["."]`, `asyncio_mode = "strict"`, `addopts = "-q"`)
- [x] **T6** Fiche de cadrage méthodologique : justification ML supervisé (critères a, b, c, d de l'arbre de décision Larhlimi)
- [x] **T7** Rapport de conception initiale (`docs/cadrage/rapport_conception_initiale.md`)
- [x] **T8** `.github/workflows/ci.yml` : pipeline CI (pytest, ruff, mypy)

## Semaine 2 — TP2 : Pipeline ML & entraînement

- [x] **T9** `src/train.py` : pipeline TF-IDF (1-2 grammes, sublinear_tf) + LogisticRegression (class_weight=balanced, max_iter=1000)
- [x] **T10** Découpage stratifié train/test (80/20) AVANT vectorisation (pas de fuite de données)
- [x] **T11** `src/predict.py` : chargement du modèle, prédiction avec score de confiance, seuil d'abstention 0.60
- [x] **T12** Variable d'environnement `INCIDENTS_MODELE` pour découplage modèle/code (standard TP6)
- [x] **T13** `models/metrics.json` : métriques versionnées (F1-macro, accuracy, n_train, n_test, classes, date, seuil_f1)
- [x] **T14** `models/incidents.joblib` : modèle binaire (EXCLU de Git via `.gitignore`)
- [x] **T15** `data/all_tickets_processed_improved_v3.csv` : dataset 47 837 tickets IT (EXCLU de Git)
- [x] **T16** Re-entraînement du modèle pour cohérence de version (scikit-learn 1.9.1) : F1-macro = 0.857
- [x] **T17** `tests/test_week2_train.py` : test d'entraînement sur DataFrame + prédiction + cohérence seuil d'abstention

## Semaine 3 — TP3 : API REST FastAPI

- [x] **T18** `app/main.py` : application FastAPI, lifespan (chargement modèle au démarrage), CORS
- [x] **T19** `GET /health` : endpoint de santé, retourne statut + nom du modèle
- [x] **T20** `POST /predict` : réception JSON (`text`), validation Pydantic, retour catégorie + score + statut
- [x] **T21** `app/schemas.py` : schémas Pydantic v2 (`PredictRequest`, `PredictResponse`, `HealthResponse`), validation longueur (1-2000 chars)
- [x] **T22** `app/model.py` : pont `IncidentsClassifier` important directement depuis `incidents_app.predict` (pas de duplication)
- [x] **T23** Codes d'erreur : 200 (succès), 422 (validation), 503 (modèle non chargé), 500 (erreur interne)
- [x] **T24** `tests/test_integration.py` : tests `/health`, `/predict`, `/predict` texte vide 422, champ manquant 422

## Semaine 4 — TP4 : Tests avancés & MLOps

- [x] **T25** `tests/test_limites.py` : texte trop long (>2000 chars) → 422, texte vide → 422
- [x] **T26** `tests/test_jeu_or.py` : jeu d'or 14 cas clairs + 4 cas ambigus (xfail documenté) pour honnêteté académique
- [x] **T27** Seuil d'incertitude : `VALIDE` si score >= 0.60, sinon `A_VERIFIER` / `INDETERMINE`
- [x] **T28** `ruff` configuré (`line-length = 100`, select E4/E7/E9/F/I/B) — tous les checks passent
- [x] **T29** `mypy` configuré avec overrides pour joblib/sklearn/pandas — `Success: no issues found`
- [x] **T30** `.pre-commit-config.yaml` : hooks ruff + mypy à chaque commit

## Semaine 5 — TP5 : Interface Streamlit découplée

- [x] **T31** `ui/client.py` : client HTTP (`httpx.Client`), méthodes `creer_session()`, `sante()`, `predire()`, `predire_lot()`, `resumer()`
- [x] **T32** `ui/app.py` : interface Streamlit, appelle l'API via client (jamais le modèle directement), onglets "Un ticket" / "Fichier lot"
- [x] **T33** Séparation des responsabilités : UI ne connaît pas `predict()` ni le `.joblib`
- [x] **T34** Variable d'environnement `API_URL` pour pointer vers l'API (défaut `http://127.0.0.1:8000`)
- [x] **T35** `tests/test_client.py` : tests du client HTTP (à compléter si nécessaire)

## Semaine 6 — TP6 : Packaging & Dockerisation

- [x] **T36** `incidents_app/__init__.py` : paquet installable, `__version__ = "0.6.0"`
- [x] **T37** `incidents_app/predict.py` : `chemin_modele()`, `charger_modele()`, `predire()`, `ModeleIntrouvable`, seuil 0.60
- [x] **T38** `incidents_app/cli.py` : Click group, `incidents --version`, `incidents predict`, `incidents serve`
- [x] **T39** `pyproject.toml` : entry point mis à jour `incidents = "incidents_app.cli:main"`, packages `["incidents_app*", "app*", "ui*"]`
- [x] **T40** `src/predict.py` : wrapper rétrocompatible déléguant à `incidents_app.predict` (source de vérité unique)
- [x] **T41** `app/model.py` : importe directement depuis `incidents_app.predict` (architecture propre, pas de sys.path)
- [x] **T42** `Dockerfile` : image Python 3.11-slim, `pip install -r requirements.txt`, expose 8000, CMD uvicorn `app.main:app`
- [x] **T43** `docker-compose.yml` : services `api` (port 8000) et `ui` (port 8501), variables d'environnement, volumes modèle
- [x] **T44** `.dockerignore` : exclusion des artefacts (`.venv`, `*.joblib`, `*.csv`, `dist/`, `build/`, tests, docs)
- [x] **T45** Build de la roue : `incidents_app-0.6.0-py3-none-any.whl` généré avec succès
- [x] **T46** Installation editable : `pip install -e .` → `incidents --version` → `incidents-app 0.6.0`
- [x] **T47** CLI fonctionnelle : `incidents predict "Impossible de se connecter au VPN"` retourne catégorie + score + statut

## Semaine 7+ — Qualité & reproductibilité

- [x] **T48** `pytest` : 25 passed, 4 xfailed (cas ambigus documentés), 0 failed
- [x] **T49** `ruff check .` : All checks passed
- [x] **T50** `mypy incidents_app app ui src` : Success: no issues found
- [x] **T51** `models/metrics.json` à jour (F1-macro 0.857, date 2026-11-04, 8 classes)
- [x] **T52** `CONTEXTE_PROJET.md` : roadmap mise à jour (Semaine 6 = ✅)
- [x] **T53** `README.md` : architecture, installation, CLI, Docker, règles MLOps

---

## Semaine 9 — Mini-RAG (Base vectorielle de runbooks IT)

- [x] **T54** `incidents_app/rag.py` (wrapper `src/rag.py`) : classe MiniRAG avec ChromaDB (base vectorielle locale) + sentence-transformers (embeddings all-MiniLM-L6-v2), dossier surchargeable via `INCIDENTS_RUNBOOKS`
- [x] **T55** `data/runbooks/README.md` : documentation des 8 runbooks par catégorie ML
- [x] **T56** `data/runbooks/Hardware.md` : procédure dépannage matériel (écran, clavier, imprimante)
- [x] **T57** `data/runbooks/Access.md` : procédure accès (VPN, mot de passe, compte verrouillé)
- [x] **T58** `data/runbooks/Storage.md` : procédure stockage (disque plein, quota, sauvegarde)
- [x] **T59** `data/runbooks/Purchase.md` : procédure achat (licence, poste de travail)
- [x] **T60** `data/runbooks/HR Support.md` : procédure RH (congé, onboarding, admin rights)
- [x] **T61** `data/runbooks/Internal Project.md` : procédure projet interne (jalon, suivi)
- [x] **T62** `data/runbooks/Miscellaneous.md` : procédure demandes diverses
- [x] **T63** `data/runbooks/Administrative rights.md` : procédure droits administratifs
- [x] **T64** `scripts/indexer_runbooks.py` : script d'indexation des runbooks dans ChromaDB
- [x] **T65** `tests/test_rag.py` : tests d'indexation, recherche par catégorie, source citée

## Semaine 10 — IA Agentique (Résolution autonome)

- [x] **T66** `incidents_app/agent.py` (wrapper `src/agent.py`) : classe IncidentAgent (qualification ML + résolution RAG + seuil d'abstention)
- [x] **T67** `app/schemas.py` : schémas ResolveRequest / ResolveResponse (Pydantic v2)
- [x] **T68** `app/main.py` : endpoint `POST /resolve`, agent chargé dans le lifespan
- [x] **T69** `ui/client.py` : méthode `resoudre()` appelant `/resolve`
- [x] **T70** `ui/app.py` : onglet "Résolution agentique" (ML + RAG) avec affichage runbook + sources
- [x] **T71** `tests/test_agent.py` : tests résolution ticket clair, seuil d'abstention, source citée
- [x] **T72** `.gitignore` : exclusion `chroma_db/`, autorisation `data/runbooks/`
- [x] **T73** `docs/architecture_agent.md` : design de l'agent, flux, seuils, règles Larhlimi
- [x] **T74** `CONTEXTE_PROJET.md` : roadmap S9-S10 passée à ✅, architecture agentique

---

## 📊 Métriques finales (modèle entraîné sur 47 837 tickets)

| Métrique | Valeur |
|----------|--------|
| F1-macro | 0.857 |
| Accuracy | 0.857 |
| Classes | Access, Administrative rights, HR Support, Hardware, Internal Project, Miscellaneous, Purchase, Storage |
| Seuil d'abstention | 0.60 |
| Version scikit-learn | 1.9.1 (cohérence modèle/runtime) |
| Version pandas | 3.1.1 |
| Version Python | 3.13.9 |

---

## 🎯 Roadmap (phases du cours + projet 4 semaines)

| Phase | Livrable | Statut |
|-------|----------|--------|
| **Atelier 0** | Cadrage, choix de l'approche, dépôt Git, fiches de cadrage | ⏳ Cadrage projet ✅ ; trois fiches de cas du cours à compléter |
| **TP1** | API d'inférence FastAPI + modèle Scikit-learn (`/predict`, `/health`) | ✅ |
| **TP2** | Sécurisation API par `X-API-Key`, `.env.example`, client inter-services | ⬜ À faire |
| **TP3** | Interface Streamlit + mode batch CSV + graphiques | ⏳ UI unitaire ✅ ; batch CSV ⬜ |
| **TP4** | Paquet Python `v1.0.0` : wheel + sdist, `CHANGELOG.md`, tag `v1.0.0`, `verifier_livrable.py` | ⏳ Wheel `0.6.0` ✅ ; sdist/tag/CHANGELOG/script ⬜ |
| **Projet S1** | Dossier de lancement : Descriptif, Dataset, Maquette, Pipeline | ✅ |
| **Projet S2** | Modèle ML, API, interface Streamlit | ✅ |
| **Projet S3** | RAG extractif, agent autonome, packaging, Docker | ✅ |
| **Projet S4** | Tests, CI verte, gel du code, soutenance | ✅ |

**Le socle du projet est complet ; les phases TP2, TP3 (batch) et TP4 restent à finaliser pour l'alignement total avec le Volume 1 du cours.**

---

*Journal mis à jour le 2026-11-09. Conforme aux standards du cours (M. A. Larhlimi) : pas de `.joblib`/`.csv`/`.venv` dans Git, seuil d'incertitude, journal sincère des erreurs, architecture modulaire, approche RAG extractif (pas de génératif seul). La défense du RAG et les coûts mesurés sont dans [`docs/decisions/justification_rag.md`](decisions/justification_rag.md).*
