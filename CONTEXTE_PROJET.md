# CONTEXTE DU PROJET : IT Incident Classification (incidentsIT)

> **Module :** Développement et déploiement d'applications intelligentes (2026-2027)  
> **Enseignant :** M. A. Larhlimi  
> **Binôme :** Ishak Lamzouri (Membre A) & Ismail Amrani (Membre B)  
> **Dépôt :** https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20  
> **Version :** 0.6.0  
> **Dernière mise à jour :** 2026-11-09  
> **Architecture appliquée :** conforme aux phases du cours (Atelier 0 → TP1 → TP2 → TP3 → TP4 → projet 4 semaines), propre au domaine IT Incidents

---

## 📋 État Global

| Élément | Valeur |
|---------|--------|
| Statut global | ✅ Semaines 2-6 + S9-S10 complètes ; phases TP2-TP4 en cours de finalisation |
| Modèle ML | TF-IDF (1-2g) + LogisticRegression, F1-macro 0.857 |
| Dataset | 47 837 tickets IT, 8 classes |
| API REST | FastAPI, `/health`, `/predict`, `/resolve` |
| Agent | `IncidentAgent` : ML → RAG, seuil d'abstention 0,60 |
| RAG | Mini-RAG extractif local : 8 runbooks, ChromaDB 21,9 Mo, 0 €/requête |
| UI | Streamlit découplé (appelle l'API via client HTTP) |
| Packaging | Paquet `incidents_app`, entry point `incidents`, roue `0.6.0` |
| Dockerisation | `Dockerfile` + `docker-compose.yml` (Semaine 6) |
| Tests | 42 passed, 4 xfailed, 0 failed |
| Qualité | ruff: All checks passed / mypy: no issues found (22 fichiers) |
| CI/CD | GitHub Actions (`.github/workflows/ci.yml`) |

---

## 🏗️ Architecture (Conforme TP1-TP6, règles Larhlimi)

```
incidentsIT/
├── .github/workflows/ci.yml      # CI : pytest, ruff, mypy
├── Dockerfile                    # Semaine 6 : image production (python:3.11-slim)
├── docker-compose.yml            # Semaine 6 : api (8000) + ui (8501)
├── .dockerignore                 # Artefacts exclus du build Docker
├── pyproject.toml                # PEP 621, entry point incidents = incidents_app.cli:main
├── requirements.txt              # Versions épingrées (reproductibilité)
├── .gitignore                    # Strict : pas de .venv, *.joblib, *.csv, dist, build
├── Makefile                      # Raccourcis setup/test/check
├── README.md                     # Documentation utilisateur + Docker
├── CONTEXTE_PROJET.md            # Ce document (état, roadmap, métriques)
├── Briefing_Projet_Agent_IT.md   # Cahier des charges du prof Larhlimi
├── incidents_app/                # Paquet installable (source de vérité : predict.py, rag.py, agent.py, cli.py)
├── app/                          # API FastAPI (main.py, model.py, schemas.py)
├── ui/                           # Interface Streamlit (app.py, client.py)
├── src/                          # Scripts & wrappers rétrocompatibles (train.py, predict.py, rag.py, agent.py, cli.py, ...)
├── models/                       # incidents.joblib (EXCLU Git), metrics.json (versionné)
├── data/                         # all_tickets_processed_improved_v3.csv (EXCLU Git), runbooks/ (versionnés)
├── data/runbooks/                # Runbooks IT pour Mini-RAG (versionnés, 8 catégories + README)
├── chroma_db/                    # Base vectorielle RAG (EXCLU Git, générée par scripts/indexer_runbooks.py)
├── tests/                        # Suite pytest (42 passed, 4 xfailed)
├── docs/                         # journal_tp1_tp6.md, architecture_agent.md, cadrage/, captures/
├── Dockerfile                    # S6-S10 : image production (python:3.11-slim)
├── docker-compose.yml            # S6-S10 : api (8000) + ui (8501)
├── .dockerignore                 # Artefacts exclus du build Docker
└── scripts/                      # check_setup.py, setup.sh, setup.ps1, indexer_runbooks.py
```

---

## 🔌 Pipeline MLOps

| Étape | Composant | Détail |
|-------|-----------|--------|
| S2 | Entraînement | `src/train.py` : TF-IDF + LogisticRegression, découpage stratifié 80/20 |
| S3 | API | `app/main.py` : FastAPI, lifespan, `/health`, `/predict`, codes 200/422/503/500 |
| S5 | UI | `ui/app.py` + `ui/client.py` : Streamlit découplé, client HTTP `httpx` |
| S6 | Packaging | `incidents_app/` : paquet PEP 621, Click CLI, roue buildable |
| S6 | Docker | `Dockerfile` (3.11-slim, port 8000) + `docker-compose.yml` (api + ui) |
| S9 | Mini-RAG | `incidents_app/rag.py` (wrapper `src/rag.py`) : ChromaDB + sentence-transformers, `data/runbooks/` (8 catégories), `scripts/indexer_runbooks.py` |
| S10 | IA Agentique | `incidents_app/agent.py` (wrapper `src/agent.py`) : agent autonome (ML → RAG), endpoint `POST /resolve`, UI onglet agentique |

**Modèle :** TF-IDF `ngram_range=(1,2)`, `min_df=2`, `sublinear_tf=True` + `LogisticRegression` `max_iter=1000`, `class_weight="balanced"`, `random_state=42`

**Métriques (models/metrics.json) :**
- `f1_macro`: 0.857
- `accuracy`: 0.857
- `n_train`: 38 269
- `n_test`: 9 568
- `seuil_f1`: 0.85
- `classes`: Access, Administrative rights, HR Support, Hardware, Internal Project, Miscellaneous, Purchase, Storage

**Seuil d'abstention :** 0.60 → `VALIDE` si score >= 0.60, sinon `A_VERIFIER` / `INDETERMINE`

---

## 🗺️ Roadmap (phases du cours + projet 4 semaines)

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

*Le détail du projet 4 semaines (T1–T12, Gantt, charge) est dans [`docs/semaine1/4-pipeline.md`](docs/semaine1/4-pipeline.md). Les statuts ⬜/⏳ ci-dessus sont volontairement sincères : ils indiquent les phases du cours encore à finaliser.*

---

## ⚖️ Règles de rigueur académique (Larhlimi's Standards)

1. **Zéro commit** de `*.csv`, `*.joblib`, `.venv/` — `.gitignore` strict configuré
2. Seul `models/metrics.json` est versionné (contrat de performance CI)
3. **Aucun commit direct sur `main`** : branches `feat/...`, PR relue, CI verte
4. Code modulaire, documenté, exécutable en 3 commandes sur machine vierge
5. `docs/` avec journal de bord sincère (analyse des erreurs de prédiction)
6. Arbre de décision Larhlimi : Règles métier → ML → RAG → Génératif seul (on ne saute jamais au génératif)
7. Variable d'environnement `INCIDENTS_MODELE` pour le découplage modèle/code (standard TP6)
8. L'UI n'importe jamais le modèle : elle appelle l'API via client HTTP uniquement
9. Approche RAG (S9-S10) : l'agent qualifie avec ML puis résout avec des runbooks cités (jamais de génératif seul). Seuil d'incertitude : score < 0.60 → A_VERIFIER, intervention humaine requise.

---

## 🚀 Commandes de vérification (exécuter dans `/projet_incidentsIT`)

```powershell
# 1. Activer l'environnement
.venv\Scripts\Activate.ps1

# 2. Installer le paquet (editable)
pip install -e .

# 3. Vérifier la CLI
incidents --version
incidents predict "Impossible de se connecter au VPN"

# 4. Lancer les tests
pytest -q                      # attendu : 42 passed, 4 xfailed, 0 failed

# 5. Vérifier la qualité du code
ruff check .                   # attendu : All checks passed
mypy incidents_app app ui src  # attendu : Success: no issues found

# 6. Lancer l'API
uvicorn app.main:app --reload --port 8000

# 7. Lancer l'UI (dans un autre terminal, API déjà démarrée)
streamlit run ui/app.py

# 8. Docker (Semaine 6)
docker build -t incidents-app:latest .
docker-compose up --build
```

---

## 📚 Documents associés

- `docs/semaine1/` — Dossier de lancement officiel de la Semaine 1 (Livrables 1 à 4 validés)
- `docs/suivi_semaines/` — Suivi hebdomadaire structuré des livrables (Semaines 1 à 4)
- `data/sample/` — Échantillon représentatif de 120 tickets équilibrés (`tickets_sample.csv`)
- `docs/journal_tp1_tp6.md` — Journal de bord détaillé (points T0 à T74)
- `docs/cadrage/rapport_conception_initiale.md` — Rapport de cadrage initial
- `docs/decisions/justification_rag.md` — Défense du RAG extractif (critères b et c, coûts mesurés)
- `Briefing_Projet_Agent_IT.md` — Cahier des charges du prof Larhlimi
- `README.md` — Guide d'installation et d'utilisation

---

*Document généré et maintenu par le binôme Lamzouri-Ishak / Amrani-Ismail. Conforme aux exigences du module "Développement et déploiement d'applications intelligentes" (M. A. Larhlimi, 2026-2027).*
