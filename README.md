# 🤖 Agent Autonome de Résolution d'Incidents IT

[![CI Tests](https://img.shields.io/badge/CI-GitHub_Actions-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)]()
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)]()
[![Licence](https://img.shields.io/badge/License-Academic-lightgrey)]()

> **Module :** Développement et déploiement d’applications intelligentes (2026-2027)  
> **Enseignant :** M. A. Larhlimi  
> **Équipe de développement (Binôme) :**
> - **Ishak Lamzouri** ([@inazuma2004](https://github.com/inazuma2004))
> - **Ismail Amrani** ([@Amaranix](https://github.com/Amaranix))  
> **Dépôt officiel GitHub :** [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20)

---

## 📌 Présentation du Projet

Ce projet a pour objectif de concevoir, déployer et exploiter en production un **système intelligent et agentique dédié à la gestion autonome d'incidents informatiques (IT Helpdesk)**. 

Conformément à la grille de cadrage méthodologique du cours, notre architecture logicielle combine deux mondes complémentaires :
1. **Une brique de Machine Learning classique (NLP supervisé)** pour classifier et router instantanément les descriptions d'incidents utilisateurs vers la bonne catégorie avec un calcul de score d'incertitude.
2. **Une brique IA Agentique et Mini-RAG (Semaines 9-10)** où l'agent autonome prend en charge la catégorie qualifiée, extrait la procédure de dépannage adéquate (runbook) depuis une base vectorielle, et fournit la solution directement à l'utilisateur.

---

## 🎬 Vidéos de Soutenance & Cadrage Initial

Dans le cadre du premier livrable (Cadrage et Choix d'Approche), les deux vidéos de présentation du binôme sont disponibles dans [`docs/media/`](docs/media/) :
* 📹 **Vidéo d'Ismail Amrani :** [`docs/media/presentation_cadrage_Amrani_Ismail.mp4`](docs/media/presentation_cadrage_Amrani_Ismail.mp4)
* 📹 **Vidéo d'Ishak Lamzouri :** [`docs/media/presentation_cadrage_Lamzouri_Ishak.mp4`](docs/media/presentation_cadrage_Lamzouri_Ishak.mp4)
* 📜 **Scripts minutés et argumentations scientifiques :** [`docs/media/README.md`](docs/media/README.md)
* 📄 **Rapport de cadrage complet :** [`docs/cadrage/rapport_conception_initiale.md`](docs/cadrage/rapport_conception_initiale.md)

---

## 📊 Le Dataset Retenu

* **Nom :** [IT Service Ticket Classification Dataset sur Kaggle](https://www.kaggle.com/datasets/adisongoh/it-service-ticket-classification-dataset)
* **Volumétrie :** 47 837 tickets réels d'assistance informatique
* **Format :** CSV (`all_tickets_processed_improved_v3.csv`)
* **Variables principales :**
  * `Document` ($X$) : Texte libre saisi par l'utilisateur (*ex: "Unable to connect to internal VPN server"*).
  * `Topic_group` ($y$) : Catégorie d'incident (*Hardware, Access, Storage, HR Support, Purchase, etc.*).
* **Documentation détaillée du dataset :** [`data/README.md`](data/README.md)

---

## 🎯 Justification Scientifique de l'Approche (Grille du Cours)

En suivant l'arbre décisionnel officiel de **M. Larhlimi** :
- **Pourquoi pas de simples Règles Métier ?** La diversité linguistique et le jargon des utilisateurs rendent la formulation des pannes non figée et non déterministe.
- **Pourquoi le Machine Learning Supervisé pour la méthode 1 ?**
  - **Critère (a) - Données étiquetées :** Nous disposons de 47 800+ tickets déjà annotés par des techniciens.
  - **Critère (b) - Vérifiabilité :** Évaluation sur un jeu de test disjoint via $F_1$-score macro et audit des n-grammes TF-IDF.
  - **Critère (c) - Coût et Latence :** L'inférence sur CPU prend moins de 5 millisecondes avec une empreinte mémoire minime, évitant tout GPU payant en production.
  - **Critère (d) - Conséquence d'une erreur :** Risque faible, sécurisé dans l'interface par un seuil d'incertitude réorientant les cas ambigus vers un opérateur humain.

---

## 📂 Architecture Structurée du Dépôt

Le dépôt est organisé selon les standards stricts du génie logiciel et du MLOps :

```text
Lamzouri_Ishak-Amrani_Ismail/
├── .github/
│   └── workflows/              # Pipelines d'intégration continue CI/CD (GitHub Actions)
├── data/                       # Documentation et gestion des données (données brutes ignorées par Git)
│   ├── README.md               # Guide d'obtention du dataset Kaggle
│   └── runbooks/               # Base de connaissances RAG (8 runbooks Markdown versionnés)
├── docs/                       # Rapports, cadrage et médias
│   ├── cadrage/                # Rapports d'étude de conception et fiches de cadrage
│   │   └── rapport_conception_initiale.md
│   ├── architecture_agent.md    # Design Mini-RAG + IA agentique (S9-S10)
│   └── media/                  # Vidéos de cadrage et scripts de présentation
│       ├── presentation_cadrage_Lamzouri_Ishak.mp4
│       └── README.md
├── models/                     # Métriques versionnées (les binaires lourds .joblib sont exclus)
│   └── metrics.json            # Contrat de performance testé par la CI
├── chroma_db/                  # Base vectorielle RAG locale (générée, exclue de Git)
├── incidents_app/              # Paquet Python installable (predict, rag, agent, cli) — source de vérité
├── src/                        # Logique métier et pipeline de Machine Learning (train, predict, rag, agent)
├── app/                        # API REST FastAPI (endpoints /predict, /resolve, /health...)
├── ui/                         # Interface utilisateur interactive Streamlit (2 onglets : ML et agent)
├── tests/                      # Suite de tests automatisés pytest (42 passed, 4 xfailed)
├── scripts/                    # Scripts utilitaires (setup, vérification, indexation_runbooks.py)
├── Dockerfile                  # Semaine 6 : image de production (uvicorn app.main:app)
├── docker-compose.yml          # Semaine 6 : déploiement local (api + ui)
├── .dockerignore               # Artefacts exclus du build Docker
├── Briefing_Projet_Agent_IT.md # Briefing de cadrage de l'équipe
├── requirements.txt            # Dépendances Python du projet
├── .gitignore                  # Exclusion stricte des artefacts lourds (.venv, .joblib, data/*.csv)
└── README.md                   # Présentation générale du projet
```

---

## ⚙️ Règles de Collaboration & MLOps pour le Binôme

1. **Aucun commit direct sur la branche `main` :**
   - Chaque fonctionnalité est développée sur une branche dédiée (`feat/nom-fonctionnalite`).
   - Une Pull Request (PR) est ouverte, relue et approuvée par le binôme avant fusion.
2. **Ce qui est versionné vs non versionné :**
   - Le fichier `models/metrics.json` est **toujours versionné** pour tracer les performances dans la CI.
   - Les modèles binaires (`*.joblib`), le dossier d'environnement virtuel (`.venv/`) et les gros fichiers de données brutes (`*.csv`) sont **strictement exclus** par le `.gitignore`.
3. **Reproductibilité :**
   - L'environnement s'installe en quelques commandes sur n'importe quel ordinateur portable standard.

---

## 🚀 Installation & Démarrage Rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20.git
cd Lamzouri_Ishak-Amrani_Ismail

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
# Sous Windows :
.venv\Scripts\activate
# Sous Linux/Mac :
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Installer le paquet en mode editable (commande `incidents`)
pip install -e .

# 5. Vérifier la CLI
incidents --version
incidents predict "Impossible de se connecter au VPN"

# 6. Indexer les runbooks IT dans la base vectorielle RAG (obligatoire une fois)
python scripts/indexer_runbooks.py
```

---

## 🧠 Mini-RAG & Agent Autonome (Semaines 9-10)

L'agent suit strictement l'arbre de décision du cours : **ML → RAG** (jamais de génératif seul).

### Pourquoi un RAG extractif ? (défense)

Le RAG n'est utilisé que pour la **résolution**, jamais pour la classification (le ML reste le moteur de qualification, car 47 837 tickets étiquetés existent).

- **(b) Vérifiabilité :** chaque réponse `VALIDE` renvoie le **texte exact du runbook** et le **chemin de la source** (`data/runbooks/*.md`), versionné dans Git. Aucune reformulation par un LLM.
- **(c) Coût par requête :** **0 €** de coût marginal, **23 ms** de CPU par requête (p95 : 25,36 ms), index ChromaDB **21,9 Mo**, modèle d'embedding **87,3 Mo**, aucun GPU, aucun token. À 1 000 tickets/jour : environ **23 secondes de CPU cumulées**.

Pourquoi pas un LLM génératif seul ? Il serait facturé au token, introduirait une latence réseau, ne garantirait pas la source et pourrait inventer une commande. Le cours accepte ce coût pour « quelques dizaines de questions par jour » ; notre volume est de **centaines de tickets par jour**. Le RAG extractif conserve le **R** (retrieval) et remplace le **G** (generation) par une extraction verbatim.

> 📘 Défense complète, protocole de mesure, comparaison RAG vs génératif et limites : [`docs/decisions/justification_rag.md`](docs/decisions/justification_rag.md)

### Fonctionnement

1. **Qualification ML** (`incidents_app/predict.py`) : catégorie + score de confiance.
2. **Seuil d'incertitude** : si `score < 0.60` → statut `A_VERIFIER`, **aucune résolution automatique**, renvoi vers un opérateur humain.
3. **Résolution RAG** (`incidents_app/rag.py`, wrapper `src/rag.py`) : recherche du runbook de la catégorie prédite dans ChromaDB (embeddings `all-MiniLM-L6-v2`), avec **source citée** (chemin + score).

### Base de connaissances

8 runbooks versionnés dans [`data/runbooks/`](data/runbooks/) (un par catégorie : Access, Administrative rights, HR Support, Hardware, Internal Project, Miscellaneous, Purchase, Storage). Chaque runbook contient symptômes, procédure numérotée, escalade et temps estimé.

### Utilisation en ligne de commande

```bash
# Indexer (ou ré-indexer) les runbooks
python scripts/indexer_runbooks.py

# Résoudre un incident de bout en bout
python -m src.agent "cannot login vpn password expired please reset account locked"

# Recherche RAG ciblée (catégorie, requête)
python -m src.rag --rechercher Hardware "ecran noir qui scintille"
```

### API & UI

```bash
# API : endpoint POST /resolve
uvicorn app.main:app --reload
# Docs interactives : http://localhost:8000/docs

# UI Streamlit : onglet « Résolution agentique (ML + RAG) »
streamlit run ui/app.py
```

Exemple d'appel API :

```bash
curl -X POST http://localhost:8000/resolve \
  -H "Content-Type: application/json" \
  -d '{"text": "cannot login vpn password expired"}'
```

La réponse contient : `categorie`, `score`, `statut` (`VALIDE`/`A_VERIFIER`), `runbook`, `resolution`, `sources` et `action_humaine`.

> 📘 Design détaillé, flux et justification : [`docs/architecture_agent.md`](docs/architecture_agent.md)

---

## 🐳 Dockerisation (Semaine 6)

```bash
# Construire l'image
docker build -t incidents-app:latest .

# Lancer l'API seule (monter le modèle entraîné, exclu de l'image)
docker run -p 8000:8000 \
  -v "$(pwd)/models:/app/models:ro" \
  -e INCIDENTS_MODELE=/app/models/incidents.joblib \
  incidents-app:latest

# Ou avec docker-compose (API + UI)
docker-compose up --build
```

---

## 👥 Auteurs
- **Ishak Lamzouri** - [@inazuma2004](https://github.com/inazuma2004)
- **Ismail Amrani** - [@Amaranix](https://github.com/Amaranix)
