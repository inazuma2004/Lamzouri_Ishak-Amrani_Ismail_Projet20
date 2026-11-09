# 🚀 Traçabilité du Projet Final & Feuille de Route (Prochaine Conversation)

> **Projet :** Agent Autonome de Résolution d'Incidents IT (IT Helpdesk)  
> **Dépôt Git :** [https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20](https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20)  
> **Branche :** `main`  
> **Auteurs :** Ishak Lamzouri ([@inazuma2004](https://github.com/inazuma2004)) & Ismail Amrani ([@Amaranix](https://github.com/Amaranix))

---

## 📌 1. Ce qui a été fait (Livrables Initiaux)

1. **Cadrage méthodologique complet :**
   - Justification de l'approche hybride : Machine Learning supervisé (classification/routag
   e rapide) + Agent RAG (recherche contextuelle de runbooks et résolution autonome).
   - Validation des critères du cours : Données étiquetées disponibles ($N = 47\,837$), vérifiabilité par $F_1$-score macro, coût d'inférence < 5ms sur CPU, mitigeage d'erreur via seuil d'incertitude.
   - Rapport initial disponible dans `docs/cadrage/rapport_conception_initiale.md`.

2. **Dépôt Git & Squelette logiciel :**
   - Dépôt configuré avec GitHub Actions (`.github/workflows/ci.yml`).
   - Structure modulaire : `src/` (ML pipeline), `app/` (API FastAPI), `data/` (documentation Kaggle), `tests/` (pytest).
   - Vidéos de cadrage et scripts enregistrés et référencés.

---

## 🎯 2. Feuille de Route pour la Prochaine Conversation

Pour démarrer efficacement la suite du projet, les étapes prioritaires sont :

### Étape 1 : Téléchargement & Intégration du Dataset IT Tickets
- Télécharger le fichier CSV `all_tickets_processed_improved_v3.csv` depuis Kaggle et le placer dans `projet_incidentsIT/data/`.
- S'assurer que le `.gitignore` empêche son suivi direct dans Git (données volumineuses).

### Étape 2 : Pipeline d'Entraînement de Modèle (`src/train.py`)
- Créer un pipeline Scikit-Learn : vectorisation TF-IDF (1 à 2-grammes, sous-linéaire) couplée à un classifieur multiclasse (ex: `LogisticRegression` ou `LinearSVC`).
- Évaluer les métriques ($F_1$ macro, précision, rappel par catégorie de ticket : Hardware, Access, Network, etc.).
- Exporter les métriques dans `models/metrics.json` pour la validation CI.

### Étape 3 : API Backend FastAPI (`app/main.py`)
- Endpoint `/predict` recevant le texte du ticket et renvoyant :
  - La catégorie prédite.
  - La probabilité de confiance.
  - Le statut d'incertitude (`VALIDE` ou `A_VERIFIER`).
- Endpoint `/health` pour le monitoring de l'agent.

### Étape 4 : Mini-Moteur Agentique RAG
- Indexer une base de connaissances locale (runbooks IT au format Markdown/JSON).
- Recommander la procédure de résolution exacte basée sur la catégorie qualifiée.

### Étape 5 : Interface Utilisateur Streamlit (`ui/app.py`)
- Formulaire pour soumettre un incident en langage naturel.
- Visualisation du routage, de la confiance du modèle et de la fiche de résolution générée.
- Mode de téléversement par lot (fichier CSV de tickets à qualifier).

---

## 💡 Notes Importantes pour le Prochain Agent

- **Environnement Virtuel :** Utiliser un environnement virtuel dédié dans `projet_incidentsIT/.venv/` avec `requirements.txt`.
- **Intégrité Git :** Ne jamais commiter de fichiers `.joblib` ou `.csv` volumineux. Seul `models/metrics.json` doit être tracé.
- **Dépôt des TPs :** Le dépôt des TPs (`TPs/Tp1/`) est autonome et déjà à 100% conforme. Ne pas modifier `TPs/` lors du travail sur le projet final.
