# Finalisation projet à 100% (TP2 + TP3 + TP4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Amener `projet_incidentsIT` à 100% : ajouter la sécurisation API par clé (TP2), le traitement par lot CSV dans l'UI (TP3), et le paquet redistribuable v1.0.0 avec script de vérification (TP4), puis nettoyer les fichiers parasites.

**Architecture:** On adapte les kits officiels du prof (kit-tp2, kit-tp3, kit-tp4) au domaine incidentsIT sans les copier bêtement : `app/securite.py` (X-API-Key, rôles client/admin), `ui/client.py` (clé depuis `.env`, codes d'erreur stables), `ui/app.py` (3e onglet batch CSV), `pyproject.toml` v1.0.0 + package-data `.joblib`, `CHANGELOG.md`, `scripts/verifier_livrable.py`, `tests/test_paquet.py`, tag `v1.0.0`.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, python-dotenv, Streamlit, httpx, setuptools/wheel, pytest, ruff, mypy.

**Spec:** `TPs/seance_09_11_2026/` (manuel-tp-volume1.pdf, kit-tp2/3/4), `GRILLE-DE-DECISION.md`, `Dossier de lancement (semaine 1)`.

## Global Constraints

- Aucun `.joblib`, `.csv`, `.venv`, `dist/` dans Git (`.gitignore` strict déjà en place).
- Seul `models/metrics.json` est versionné.
- Seuil d'incertitude 0.60 conservé partout.
- Pas de plateforme payante : tout tourne sur portable, CPU seulement.
- RAG extractif déjà en place (S9-S10) : ne pas y toucher, juste s'assurer qu'il reste fonctionnel.
- Chaque nouvelle route protégée exige l'en-tête `X-API-Key` ; `/health` reste public (Docker healthcheck).
- `.env` n'est JAMAIS commité ; seul `.env.example` l'est.

## Review Focus

1. Clé API manquante sur `/predict` → 401 `WWW-Authenticate: APIKey`.
2. Clé API avec rôle `client` sur une route admin → 403 (si route admin ajoutée).
3. Fichier CSV sans colonne `Document` → 422 / message lisible dans l'UI.
4. `.env` absent en production : l'API démarre mais les routes protégées répondent 401 (fermé par défaut).
5. La roue v1.0.0 embarque `models/incidents.joblib` et expose la commande `incidents`.
6. `verifier_livrable.py` termine par `Bilan : CONFORME` sur une installation propre.

---

### Task 1: TP2 — Sécurisation API par clé d'API (X-API-Key)

**Files:**
- Create: `app/securite.py`
- Create: `.env.example`
- Modify: `app/main.py` (protéger /predict et /resolve, charger clés au lifespan, gestion erreurs 401/403)
- Create: `tests/test_securite.py`
- Modify: `ui/client.py` (ajouter header X-API-Key depuis .env, gérer codes 401/403/422/503)
- Modify: `.github/workflows/ci.yml` (passer API_KEYS aux tests d'auth)

**Interfaces:**
- `app/securite.charger_cles(brut=None) -> dict[str, Role]` — lit `API_KEYS` format `cle:role,...`, rôle client|admin, longueur min 16, `secrets.compare_digest`
- `app/securite.identifier(cle) -> Role` — 401 si absente/inconnue
- `app/securite.exiger(*roles) -> Depends` — 403 si rôle insuffisant
- `app/main.predict` / `app/main.resolve` : `Depends(exiger("client"))` ; `/health` public

- [ ] **Step 1: Créer `app/securite.py`** inspiré du kit-tp2 (charger_cles, identifier, exiger, APIKeyHeader X-API-Key, LONGUEUR_MIN=16)
- [ ] **Step 2: Créer `.env.example`** avec `API_KEYS=cle-client:client,cle-admin:admin`, `API_URL`, `API_KEY`, `CORS_ORIGINS`
- [ ] **Step 3: Modifier `app/main.py`** — importer securite, `load_dotenv()` au lifespan, protéger `/predict` et `/resolve` via `Depends(exiger("client"))`, ajouter gestionnaire d'erreurs 401/403, garder `/health` public
- [ ] **Step 4: Écrire `tests/test_securite.py`** — TestClient avec headers : 401 sans clé, 200 avec bonne clé client, 401 avec mauvaise clé
- [ ] **Step 5: Modifier `ui/client.py`** — `load_dotenv()`, header `X-API-Key` dans `creer_session()`, traduire 401/403 → message clé, 422 → refus, 503 → modèle indisponible
- [ ] **Step 6: Lancer `pytest tests/test_securite.py`** → attendu PASS
- [ ] **Step 7: Commit** `feat(tp2): securisation API par cle X-API-Key + .env.example`

### Task 2: TP3 — Interface utilisateur : traitement par lot CSV

**Files:**
- Create: `ui/graphiques_demo.py`
- Modify: `ui/app.py` (3e onglet "Traitement par lot CSV" : uploader, predire_lot, tableau, graphiques, téléchargement CSV annoté)
- Modify: `requirements.txt` (ajouter `python-dotenv`)
- Create: `tests/test_ui_batch.py` (ou étendre) — uploader CSV invalide (pas de colonne Document), CSV valide, téléchargement

**Interfaces:**
- `ui/client.predire_lot(session, textes) -> list[Reponse]`
- `ui/client.resumer(reponses) -> dict[str, int]`
- `ui/graphiques_demo` : bar_chart répartition verdicts + distribution confiance

- [ ] **Step 1: Ajouter `python-dotenv` à `requirements.txt`**
- [ ] **Step 2: Créer `ui/graphiques_demo.py`** (2 graphiques Streamlit, adaptation incidentsIT)
- [ ] **Step 3: Modifier `ui/app.py`** — 3e onglet batch : `st.file_uploader`, lecture CSV, colonne `Document`, `predire_lot`, tableau résultats, graphiques, `st.download_button` CSV annoté
- [ ] **Step 4: Créer un test de batch** — CSV sans colonne Document → erreur lisible ; CSV valide → lignes traitées
- [ ] **Step 5: Lancer `pytest` et `streamlit` smoke check** → UI importable sans erreur
- [ ] **Step 6: Commit** `feat(tp3): traitement par lot CSV dans l'UI Streamlit`

### Task 3: TP4 — Paquet Python redistribuable v1.0.0

**Files:**
- Modify: `pyproject.toml` (version 1.0.0, package-data `models/*.joblib`, entry point `incidents`, inclure `app*`, `ui*`)
- Create: `CHANGELOG.md` (section [1.0.0])
- Create: `scripts/verifier_livrable.py` (adapté incidentsIT, stdlib uniquement, rapport `docs/livrable-tp4.txt`)
- Create: `tests/test_paquet.py` (ignorés dans le dépôt, obligatoires avec VERIFICATION_LIVRABLE=1)
- Create: `.gitkeep` dans `models/` si besoin (déjà présent)
- Modify: `.gitignore` (ajouter `docs/livrable-tp4.txt` non commité)

**Interfaces:**
- `incidents_app.__version__ == "1.0.0"`
- commande `incidents predict <texte>` et `incidents --version`
- roue : `incidents_app-1.0.0-py3-none-any.whl` + sdist `.tar.gz` dans `dist/`

- [ ] **Step 1: Modifier `pyproject.toml`** — version 1.0.0, `[tool.setuptools.package-data] incidents_app = ["models/*.joblib"]`, entry point inchangé
- [ ] **Step 2: Créer `CHANGELOG.md`** avec `[1.0.0] — 2026-11-09` et liste des changements
- [ ] **Step 3: Créer `scripts/verifier_livrable.py`** — contrôle dist/ (roue + sdist), contenu roue (joblib, entry_points), CHANGELOG, tag git, install venv neuf, pytest test_paquet.py, commande `incidents`, rapport `docs/livrable-tp4.txt`
- [ ] **Step 4: Créer `tests/test_paquet.py`** — importe depuis site-packages, version 1.0.0, modèle embarqué, commande installée, texte vide refusé
- [ ] **Step 5: Tag Git `v1.0.0`** sur le dernier commit de cette task
- [ ] **Step 6: Build** `python -m build` → `dist/incidents_app-1.0.0-py3-none-any.whl` + `.tar.gz`
- [ ] **Step 7: Lancer `python scripts/verifier_livrable.py`** → `Bilan : CONFORME`
- [ ] **Step 8: Commit** `feat(tp4): paquet redistribuable v1.0.0, CHANGELOG, verifier_livrable, tag v1.0.0`

### Task 4: Nettoyage et vérification finale 100%

**Files:**
- Delete: `test.txt`, `PLAN_FINALISATION_AUJOURD_HUI.md`
- Modify: `.gitignore` (ajouter `docs/livrable-tp4.txt`)

- [ ] **Step 1: Supprimer `test.txt` et `PLAN_FINALISATION_AUJOURD_HUI.md`**
- [ ] **Step 2: Lancer `pytest -q`** → 0 failed
- [ ] **Step 3: Lancer `ruff check .`** → All checks passed
- [ ] **Step 4: Lancer `mypy incidents_app app ui src`** → Success
- [ ] **Step 5: `docker compose config`** → valide
- [ ] **Step 6: Commit final** `chore: nettoyage et verification finale 100%`

---

Ce plan couvre TP2, TP3, TP4 du manuel Volume 1 plus le nettoyage. Il ne touche pas au RAG (déjà vert S9-S10) ni aux livrables semaine 1 (déjà rédigés).