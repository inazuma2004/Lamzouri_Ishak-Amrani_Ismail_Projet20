# Semaine 9-10 : Mini-RAG & IA Agentique — incidentsIT

> **Document historique (04/11/2026).** Le RAG final est **extractif** (retrieval + runbook verbatim + source citée, sans LLM génératif) ; la justification et les coûts mesurés sont dans [`docs/decisions/justification_rag.md`](../../decisions/justification_rag.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implémenter la brique Mini-RAG (Semaine 9) et l'IA Agentique (Semaine 10) sur `projet_incidentsIT`, en s'appuyant sur l'architecture de référence `sentiment-app` et en respectant les règles du prof Larhlimi (arbre de décision : ML → RAG, pas de génératif seul, seuil d'incertitude, journal sincère).

**Architecture:**
- S9 Mini-RAG : `src/rag.py` (base vectorielle ChromaDB locale + sentence-transformers pour embeddings), `data/runbooks/` (procédures de dépannage par catégorie IT en Markdown), indexation et recherche similaire par catégorie.
- S10 IA Agentique : `src/agent.py` (agent autonome : qualifie le ticket via ML existant, récupère le runbook via RAG, retourne la résolution), endpoint API `POST /resolve`, onglet UI "Résolution agentique", tests RAG + agent.

**Tech Stack:** Python 3.11, sentence-transformers, chromadb, scikit-learn (ML existant), FastAPI, Streamlit, pytest, ruff, mypy.

**Spec:** Briefing_Projet_Agent_IT.md (Semaines 9-10), architecture Larhlimi (ML classique pour qualification + RAG pour résolution, seuil d'incertitude, pas de génératif seul).

## Global Constraints

- Pas de `.csv`, `*.joblib`, `.venv` dans Git (`.gitignore` strict existant).
- Base vectorielle Chroma (`chroma_db/`) exclue de Git (artefact lourd), seule la documentation des runbooks est versionnée.
- L'agent ne doit JAMAIS utiliser un modèle génératif seul : il qualifie avec ML (déjà en place) puis résout avec RAG (documents cités).
- Seuil d'incertitude : si le ML hésite (score < 0.60), le ticket est `A_VERIFIER` et l'agent ne résout pas automatiquement (renvoie à un humain).
- Variable d'env pour le chemin du modèle : `INCIDENTS_MODELE`.
- Code exécutable en 3 commandes sur machine vierge.

## Review Focus

- RAG retourne des sources citables (runbook cité) — pas de génératif sans source.
- Seuil d'abstention respecté : score < 0.60 → A_VERIFIER, pas de résolution automatique.
- L'agent réutilise le modèle ML existant (pas de ré-entraînement).
- Base vectorielle exclue de Git, reconstruite via script d'indexation.
- Tests RAG (recherche retourne des documents pertinents) et agent (résolution cohérente).

---

### Task 1: Ajouter dépendances RAG (requirements.txt + pyproject.toml)

**Files:**
- Modify: `requirements.txt` (ajouter sentence-transformers, chromadb)
- Modify: `pyproject.toml` (dependencies)

**Interfaces:**
- `sentence-transformers==3.2.*` (ou version compatible)
- `chromadb==0.5.*` (base vectorielle locale)

- [ ] **Step 1: Modifier requirements.txt** — ajouter sentence-transformers et chromadb avec versions épingrées
- [ ] **Step 2: Modifier pyproject.toml** — ajouter les dépendances au bloc `[project]dependencies`
- [ ] **Step 3: Vérifier** `pip install -r requirements.txt` réussit
- [ ] **Step 4: Commit** `feat: ajouter dépendances RAG (sentence-transformers, chromadb)`

### Task 2: Créer les runbooks IT (base de connaissances RAG)

**Files:**
- Create: `data/runbooks/README.md` — liste des runbooks disponibles
- Create: `data/runbooks/Hardware.md` — procédure dépannage matériel (écran, clavier, imprimante)
- Create: `data/runbooks/Access.md` — procédure accès (VPN, mot de passe, compte verrouillé)
- Create: `data/runbooks/Storage.md` — procédure stockage (disque plein, quota, sauvegarde)
- Create: `data/runbooks/Purchase.md` — procédure achat (licence, poste de travail)
- Create: `data/runbooks/HR Support.md` — procédure RH (congé, onboarding, admin rights)
- Create: `data/runbooks/Internal Project.md` — procédure projet interne (jalon, suivi)
- Create: `data/runbooks/Miscellaneous.md` — procédure divers
- Create: `data/runbooks/.gitkeep` — pour versionner le dossier vide si besoin

**Interfaces:**
- Chaque fichier Markdown contient : titre, symptômes, étapes de dépannage, escalade, temps estimé.
- Nom du fichier = catégorie exacte du modèle ML (Access, Administrative rights, HR Support, Hardware, Internal Project, Miscellaneous, Purchase, Storage).

- [ ] **Step 1: Créer data/runbooks/README.md** avec la liste et la méthode d'indexation
- [ ] **Step 2: Créer les 8 fichiers runbooks** (un par catégorie ML)
- [ ] **Step 3: Vérifier** chaque fichier existe et contient au moins : symptômes, étapes, escalade
- [ ] **Step 4: Commit** `feat: ajouter runbooks IT pour Mini-RAG`

### Task 3: Créer `src/rag.py` — base vectorielle Mini-RAG

**Files:**
- Create: `src/rag.py`

**Interfaces:**
- `class MiniRAG:` 
  - `__init__(self, persist_directory="chroma_db", collection_name="runbooks_it")`
  - `indexer_runbooks(self, runbooks_dir="data/runbooks")` — lit les .md, crée embeddings (sentence-transformers), stocke dans Chroma
  - `rechercher(self, categorie: str, requete: str, k: int = 3) -> list[dict]` — retourne les runbooks les plus pertinents pour une catégorie, avec score et source citée
  - `charger_ou_indexer(self)` — charge la base existante ou indexe si absente

- [ ] **Step 1: Créer src/rag.py** avec classe MiniRAG (ChromaDB + sentence-transformers)
- [ ] **Step 2: Vérifier** `python -c "from src.rag import MiniRAG; r = MiniRAG(); print('OK')"` fonctionne
- [ ] **Step 3: Commit** `feat: créer MiniRAG (src/rag.py)`

### Task 4: Script d'indexation des runbooks

**Files:**
- Create: `scripts/indexer_runbooks.py`

**Interfaces:**
- `main()` — instantiate MiniRAG, appeler `indexer_runbooks()`, afficher le nombre de documents indexés par catégorie.

- [ ] **Step 1: Créer scripts/indexer_runbooks.py**
- [ ] **Step 2: Vérifier** `python scripts/indexer_runbooks.py` indexe les 8 runbooks et crée chroma_db/
- [ ] **Step 3: Commit** `feat: script d'indexation des runbooks`

### Task 5: Créer `src/agent.py` — IA Agentique autonome

**Files:**
- Create: `src/agent.py`

**Interfaces:**
- `class IncidentAgent:`
  - `__init__(self, rag: MiniRAG, seuil_confiance: float = 0.60)`
  - `resoudre(self, texte_ticket: str) -> dict` — retourne `{'categorie', 'score', 'statut', 'runbook', 'resolution', 'sources', 'action_humaine'}`
    1. Qualifie le ticket avec le ML existant (`incidents_app.predict.predire`)
    2. Si score < seuil → `A_VERIFIER`, pas de résolution automatique, recommande humain
    3. Sinon, recherche le runbook via RAG pour la catégorie prédite
    4. Retourne la procédure de résolution avec sources citées
  - `qualifier(self, texte: str) -> dict` — délègue à predire()

- [ ] **Step 1: Créer src/agent.py** avec classe IncidentAgent
- [ ] **Step 2: Vérifier** `python -c "from src.agent import IncidentAgent; print('OK')"` fonctionne
- [ ] **Step 3: Commit** `feat: créer IA Agentique (src/agent.py)`

### Task 6: Endpoint API `/resolve` (FastAPI)

**Files:**
- Modify: `app/main.py` (ajouter endpoint POST /resolve)
- Modify: `app/schemas.py` (ajouter ResolveRequest, ResolveResponse)

**Interfaces:**
- `POST /resolve` — reçoit `{"text": "..."}`, retourne catégorie, score, statut, résolution RAG, sources citées, action humaine si besoin.
- Réutilise `load_model()` et `IncidentAgent` au démarrage (lifespan).

- [ ] **Step 1: Ajouter schémas ResolveRequest/ResolveResponse dans app/schemas.py**
- [ ] **Step 2: Ajouter endpoint POST /resolve dans app/main.py** (lifespan charge agent)
- [ ] **Step 3: Vérifier** l'API démarre et répond à `/resolve`
- [ ] **Step 4: Commit** `feat: endpoint API /resolve (IA Agentique)`

### Task 7: UI Streamlit — onglet "Résolution agentique"

**Files:**
- Modify: `ui/app.py` (ajouter onglet RAG/Agent)
- Modify: `ui/client.py` (ajouter méthode `resoudre()` appelant `/resolve`)

**Interfaces:**
- `ui/client.resoudre(session, texte) -> Reponse` — POST /resolve, traduit en Reponse
- `ui/app.py` — nouvel onglet "Résolution agentique" affichant catégorie, confiance, procédure RAG, sources, alerte si A_VERIFIER.

- [ ] **Step 1: Ajouter resoudre() dans ui/client.py**
- [ ] **Step 2: Ajouter onglet agentique dans ui/app.py**
- [ ] **Step 3: Vérifier** Streamlit lance sans erreur (ou syntax check)
- [ ] **Step 4: Commit** `feat: UI onglet résolution agentique`

### Task 8: Tests RAG et Agent

**Files:**
- Create: `tests/test_rag.py` — MiniRAG indexation + recherche retourne documents pertinents avec sources
- Create: `tests/test_agent.py` — IncidentAgent résolution cohérente, seuil d'abstention respecté, sources citées

**Interfaces:**
- test_rag: indexer puis rechercher "imprimante" catégorie Hardware → retourne au moins un doc avec "imprimante" ou "Hardware"
- test_agent: ticket clair Hardware → statut VALIDE + runbook non vide + sources citées; ticket ambigu → A_VERIFIER

- [ ] **Step 1: Créer tests/test_rag.py**
- [ ] **Step 2: Créer tests/test_agent.py**
- [ ] **Step 3: Vérifier** `pytest tests/` passe (33 + nouveaux tests, 0 failed)
- [ ] **Step 4: Commit** `test: ajouter tests RAG et agent`

### Task 9: Qualité code (ruff, mypy) + Docker mis à jour

**Files:**
- Modify: `Dockerfile` (ajouter sentence-transformers, chromadb déjà dans requirements)
- Modify: `docker-compose.yml` (si besoin volume chroma_db)
- Modify: `.gitignore` (ajouter chroma_db/)

**Interfaces:**
- `ruff check .` → All checks passed
- `mypy src app ui incidents_app` → no issues found
- `.gitignore` exclut `chroma_db/`

- [ ] **Step 1: Mettre à jour .gitignore** (chroma_db/)
- [ ] **Step 2: Mettre à jour Dockerfile/docker-compose** si nécessaire
- [ ] **Step 3: Vérifier** ruff + mypy propres
- [ ] **Step 4: Commit** `chore: qualité code + .gitignore chroma_db`

### Task 10: Documentation et journal de bord (Semaines 9-10)

**Files:**
- Modify: `CONTEXTE_PROJET.md` (roadmap S9-10 = [x], architecture agent)
- Modify: `docs/journal_tp1_tp6.md` (ajouter points T54-T65)
- Create: `docs/architecture_agent.md` (design de l'agent, flux, seuils)

**Interfaces:**
- Roadmap à jour.
- Journal avec points de contrôle S9-S10.
- Doc d'architecture agentique.

- [ ] **Step 1: Mettre à jour CONTEXTE_PROJET.md** (roadmap S9-10)
- [ ] **Step 2: Mettre à jour docs/journal_tp1_tp6.md** (points T54-T65)
- [ ] **Step 3: Créer docs/architecture_agent.md**
- [ ] **Step 4: Commit** `docs: semaines 9-10 RAG + agent`

### Task 11: Vérification finale complète

**Files:**
- Test: `pytest tests/`, `ruff check .`, `mypy`, `pip install -e .`, `incidents --version`, indexation runbooks, endpoint /resolve

- [ ] **Step 1: Exécuter `pip install -e .`** puis `incidents --version`
- [ ] **Step 2: Exécuter `python scripts/indexer_runbooks.py`** (indexe chroma_db)
- [ ] **Step 3: Exécuter `pytest tests/`** — confirmer tout vert
- [ ] **Step 4: Exécuter `ruff check .` et `mypy ...`** — confirmer propres
- [ ] **Step 5: Commit final** `feat: Semaines 9-10 Mini-RAG + IA Agentique terminées`

---

*Plan rédigé le 2026-11-04. Cible : amener `projet_incidentsIT` à 100% jusqu'à la Semaine 10 (dernière semaine du module).*