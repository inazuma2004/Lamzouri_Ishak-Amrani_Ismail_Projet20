# Appliquer l'architecture sentiment-app sur projet_incidentsIT

> **Document historique (04/11/2026).** Ce plan a servi de guide de structuration ; il n'est **pas** la fiche de cadrage du projet. L'architecture finale est propre au projet IT Incidents et conforme aux phases du cours (Atelier 0 → TP1 → TP2 → TP3 → TP4 → projet 4 semaines). Voir [`CONTEXTE_PROJET.md`](../../../CONTEXTE_PROJET.md) et [`docs/decisions/justification_rag.md`](../../decisions/justification_rag.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformer `projet_incidentsIT` en projet complet et conforme à l'architecture exigée par M. Larhlimi, en s'appuyant sur `sentiment-app` (TPs/Tp1/) comme modèle de référence validé. Cela inclut : paquet Python `incidents_app/`, API FastAPI qui importe depuis ce paquet, CLI complète, .gitignore strict, Dockerisation (Semaine 6), et tests qui passent.

**Architecture:** Même structure que sentiment-app : `incidents_app/` (paquet installable avec predict.py + cli.py), `app/` (FastAPI qui importe depuis incidents_app.predict via un pont model.py), `ui/` (Streamlit découplé via client HTTP), `src/` (pipeline ML existant), `tests/` (suite pytest), `.github/workflows/ci.yml` (CI), `Dockerfile` + `docker-compose.yml` (Semaine 6).

**Tech Stack:** Python 3.11, scikit-learn (TF-IDF + LogisticRegression), FastAPI, uvicorn, Streamlit, click, httpx, pydantic v2, pytest, ruff, mypy, Docker.

**Spec:** Modèle de référence = `TPs/Tp1/` (sentiment-app, 100% conforme TP1-TP5 + packaging TP6). Cible = `projet_incidentsIT/` doit atteindre le même niveau de complétude + Dockerisation (Semaine 6 en cours).

## Global Constraints

- Aucun commit de `*.csv`, `*.joblib`, `.venv/` dans Git (`.gitignore` strict, comme sentiment-app).
- Seul `models/metrics.json` est versionné (pas le binaire .joblib).
- Nom du paquet : `incidents_app` ; entry point CLI : `incidents = "incidents_app.cli:main"`.
- Variable d'environnement pour le chemin du modèle : `INCIDENTS_MODELE`.
- Seuil d'abstention : 0.6 (aligné sur TP4).
- Pas de commit direct sur `main` : branches `feat/...` + PR + CI verte (règle Larhlimi).
- Code exécutable en 3 commandes sur machine vierge.

## Review Focus

- Modèle introuvable hors dépôt sans `INCIDENTS_MODELE` → erreur claire, code 1.
- `api/model.py` n'importe jamais le .joblib directement : il passe par `incidents_app.predict`.
- `ui/` n'importe jamais le modèle : elle appelle l'API via client HTTP uniquement.
- Seuil d'abstention cohérent entre `incidents_app/predict.py` et `api/model.py`.
- `metrics.json` versionné, `incidents.joblib` et `*.csv` exclus de Git.

---

### Task 1: Créer le paquet `incidents_app/` (__init__.py, predict.py, cli.py)

**Files:**
- Create: `incidents_app/__init__.py`
- Create: `incidents_app/predict.py`
- Create: `incidents_app/cli.py`

**Interfaces:**
- `incidents_app.predict.chemin_modele() -> Path` : résout le modèle via `INCIDENTS_MODELE` ou `models/incidents.joblib`.
- `incidents_app.predict.charger_modele(chemin=None)` : charge le pipeline joblib, lève `ModeleIntrouvable`.
- `incidents_app.predict.predire(texte, modele=None) -> dict` : `{'label': ..., 'score': ...}` avec abstention sous 0.6.
- `incidents_app.cli.main` : click group, `--version`, commandes `predict` et `serve`.

- [ ] **Step 1: Créer `incidents_app/__init__.py`** avec `__version__ = "0.6.0"`
- [ ] **Step 2: Créer `incidents_app/predict.py`** (adapté de sentiment_app/predict.py, noms `incidents`, `INCIDENTS_MODELE`, `incidents.joblib`, seuil 0.6)
- [ ] **Step 3: Créer `incidents_app/cli.py`** (click group, version, `predict`, `serve` sur `api.main:app`)
- [ ] **Step 4: Vérifier** `python -c "from incidents_app import __version__; print(__version__)"` affiche `0.6.0`
- [ ] **Step 5: Commit** `feat: ajouter le paquet incidents_app (predict + cli)`

### Task 2: Mettre à jour `pyproject.toml` (nom, entry point, packages)

**Files:**
- Modify: `pyproject.toml`

**Interfaces:**
- `[project] name = "incidents-app"`, version `0.6.0`
- `[project.scripts] incidents = "incidents_app.cli:main"`
- `[tool.setuptools.packages.find] include = ["incidents_app*", "api*", "ui*"]`

- [ ] **Step 1: Modifier pyproject.toml** (nom, description, entry point, packages find)
- [ ] **Step 2: Vérifier** `pip install -e .` réussit et `incidents --version` affiche `incidents-app 0.6.0`
- [ ] **Step 3: Commit** `feat: pyproject.tomn entry point incidents`

### Task 3: Refactoriser `api/model.py` pour importer depuis `incidents_app.predict`

**Files:**
- Modify: `api/model.py`

**Interfaces:**
- `api.model.load_model() -> IncidentsClassifier` : importe `charger_modele` depuis `incidents_app.predict`, enveloppe dans `IncidentsClassifier`.
- `api.model.predict(classifier, text) -> dict` : délègue à `classifier.predict(text)`.
- `IncidentsClassifier.model_name` = `"tfidf-logreg (incidents, models/incidents.joblib)"`.

- [ ] **Step 1: Refactoriser api/model.py** pour importer depuis incidents_app.predict (plus de duplication de logique de chargement)
- [ ] **Step 2: Vérifier** `python -c "from api.model import load_model; c = load_model(); print(c.model_name)"` fonctionne
- [ ] **Step 3: Commit** `refactor: api/model importe depuis incidents_app.predict`

### Task 4: Mettre à jour `.gitignore` (modèle strict sentiment-app)

**Files:**
- Modify: `.gitignore`

**Interfaces:**
- `models/*` ignoré, sauf `!models/.gitkeep` et `!models/metrics.json`
- `data/*` ignoré, sauf `!data/.gitkeep` (et éventuellement petits CSV de test)
- `.venv/`, `__pycache__/`, `*.pyc`, `*.egg-info/`, `dist/`, `build/`, caches tests, éditeurs, PDF/ZIP, images à la racine.

- [ ] **Step 1: Réécrire .gitignore** sur le modèle de sentiment-app (adapté : incidents.joblib, all_tickets_processed_improved_v3.csv)
- [ ] **Step 2: Vérifier** `git check-ignore models/incidents.joblib data/all_tickets_processed_improved_v3.csv .venv` retourne les chemins (ils sont ignorés)
- [ ] **Step 3: Commit** `chore: .gitignore strict (pas de .joblib, .csv volumineux, .venv)`

### Task 5: Créer `Dockerfile` (Semaine 6 — Dockerisation)

**Files:**
- Create: `Dockerfile`

**Interfaces:**
- `FROM python:3.11-slim`
- Installe `requirements.txt`
- Copie le code source
- Expose `8000`
- `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`
- Variable d'env `INCIDENTS_MODELE` documentée (à passer à l'exécution si modèle hors dépôt)

- [ ] **Step 1: Créer Dockerfile** (multi-stage optionnel, slim, port 8000, CMD uvicorn app.main:app)
- [ ] **Step 2: Vérifier** `docker build -t incidents-app:test .` réussit (si Docker disponible) — sinon syntax check avec `docker config` ou lecture visuelle
- [ ] **Step 3: Commit** `feat: Dockerfile (Semaine 6 - Dockerisation)`

### Task 6: Créer `docker-compose.yml` (Semaine 6 — Déploiement)

**Files:**
- Create: `docker-compose.yml`

**Interfaces:**
- Service `api` : build depuis `.`, ports `8000:8000`, variables d'environnement `INCIDENTS_MODELE`, `API_URL`
- Dépendance implicite : le modèle doit être accessible (volume ou variable d'env)

- [ ] **Step 1: Créer docker-compose.yml** (service api, port 8000, vars d'env)
- [ ] **Step 2: Vérifier** `docker-compose config` valide (si Docker disponible)
- [ ] **Step 3: Commit** `feat: docker-compose.yml (Semaine 6 - Déploiement)`

### Task 7: Compléter les tests de base (pytest)

**Files:**
- Create: `tests/test_model.py` (ou compléter l'existant)
- Create: `tests/test_api.py` (ou compléter l'existant)
- Create: `tests/test_client.py` (ou compléter l'existant)
- Modify: `tests/conftest.py` si nécessaire

**Interfaces:**
- Au moins un test qui vérifie que `charger_modele` lève `ModeleIntrouvable` sans modèle.
- Au moins un test sur `api.schemas` (Pydantic validation).
- Au moins un test d'intégration `/health` et `/predict` via TestClient.

- [ ] **Step 1: Écrire tests/test_model.py** (ModeleIntrouvable, chargement si modèle présent)
- [ ] **Step 2: Écrire tests/test_api.py** (schémas, endpoints avec TestClient)
- [ ] **Step 3: Écrire tests/test_client.py** (client HTTP, réponses)
- [ ] **Step 4: Vérifier** `pytest -q` passe (ou au moins pas de nouvelle régression)
- [ ] **Step 5: Commit** `test: ajouter tests de base (modèle, API, client)`

### Task 8: Mettre à jour la documentation et le journal de bord

**Files:**
- Modify: `CONTEXTE_PROJET.md` (roadmap : Semaine 6 passée à [x])
- Modify: `README.md` (ajouter Docker, commande incidents, structure incidents_app)
- Create: `docs/docker.md` (ou ajouter dans docs existant) : commandes Docker, variables d'env

**Interfaces:**
- `CONTEXTE_PROJET.md` : Semaine 6 cochée.
- `README.md` : installation avec `incidents` CLI, Docker build/run.

- [ ] **Step 1: Mettre à jour CONTEXTE_PROJET.md** (Semaine 6 = [x])
- [ ] **Step 2: Mettre à jour README.md** (installation, CLI, Docker)
- [ ] **Step 3: Commit** `docs: roadmap Semaine 6 + README Docker/CLI`

### Task 9: Vérification finale complète

**Files:**
- Test: `pytest -q`, `ruff check .`, `mypy api ui src incidents_app`, `pip install -e .`, `incidents --version`, `incidents predict "..."`, `docker build` (si dispo)

- [ ] **Step 1: Exécuter `pip install -e .`** puis `incidents --version`
- [ ] **Step 2: Exécuter `pytest -q`** — confirmer que les tests passent
- [ ] **Step 3: Exécuter `ruff check .` et `mypy api ui src incidents_app`** — confirmer pas d'erreurs
- [ ] **Step 4: Exécuter `incidents predict "Impossible de me connecter au VPN"`** — affiche une catégorie + score
- [ ] **Step 5: Commit final** `feat: projet_incidentsIT conforme architecture Larhlimi (Semaine 6 OK)`

---

*Plan rédigé le 2026-11-04. Le modèle de référence est `TPs/Tp1/` (sentiment-app, 100% conforme TP1-TP5 + packaging TP6). La cible est `projet_incidentsIT/` qui doit atteindre le même niveau + Dockerisation (Semaine 6).*