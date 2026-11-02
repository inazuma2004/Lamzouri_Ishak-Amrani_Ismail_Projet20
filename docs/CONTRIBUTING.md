# 🎯 **Contrats d'entrée et de sortie de l'API**

| Point d'accès | Méthode | Entrée (type) | Sortie (type) | Description |
|--------------|--------|---------------|--------------|-------------|
| `/health` | GET | - | `HealthResponse` | État du service et nom du modèle |
| `/predict` | POST | `PredictRequest` (JSON) | `PredictResponse` (JSON) | Classification d'incident et confiance, statut basé sur seuil |

**Réponse d'erreur standard :**
```json
{"detail": "msg d'erreur"}
```

**Modèle :**
- `label` → catéqorie d'incident prédite (`Hardware`, `Access`, etc.)
- `score` → score de confiance du modèle (0–1)
- `text` → aperçu de l'entrée (premiers 100 caractères)
- `status` → `VALIDE` si le modèle est sûr, sinon `A_VERIFIER`

## 🛠️ Contribution Guidelines

### 📂 Repository Structure

- `src/` – Scripts source (entraînement, prédiction)
- `app/` – API FastAPI (`main.py`, `model.py`, `schemas.py`)
- `ui/` – Interface Streamlit (simplifiée pour le moment)
- `tests/` – Suite de tests automatisés (pytest)
- `data/` – Données brutes (ne pas commiter les CSV volumineux)
- `models/` – Modèle entraîné (`.joblib`) et métriques (`metrics.json`)

### 🚀 Quick Start (with .venv)

```bash
cd projet_incidentsIT
# Activate virtual environment (GitHub Actions creates it automatically)
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# 1. Install dependencies
pip install -r requirements.txt

# 2. Entraînez le modèle sur le dataset Kaggle
python src/train.py --csv data/all_tickets_processed_improved_v3.csv

# 3. Lancez l'API FastAPI
uvicorn app.main:app --reload --port 8000

# 4. Lancez l'interface Streamlit
streamlit run ui/app.py
```

### 🧪 Lancer les Tests

```bash
pytest -q
# Résultat attendu : tous les tests aux limites, API et entraînement passent
```

### 📈 Métriques de Performance (exemple)

| Métrique | Valeur (à mettre à jour après l'entraînement) |
|----------|----------------------------------|
| F1 macro | 0.88 (à ajuster) |
| Accuracy | 0.85 (à ajuster) |
| Seuils (INCERTEINE) | 0.60 |

### 🏷️ Conventions de Code

- **Tests aux limites** dans `tests/` pour le contrat d'entrée (`PredictRequest`)
- **Tests d'intégration** vérifient `/health` et `/predict`
- **Tests unitaires** dans `tests/test_week2_train.py`
- **Taille de batch** pour `/predict` : min=1, max=5000 caractères
- **Seuil d'incertitude** (60 %) retourne le statut `A_VERIFIER`

### 📝 Remarques Spéciales

- **API** est autonome : charge le modèle une seule fois lors du démarrage (lifespan)
- **Streamlit** consomme l'API (`ui/client.py`) et affiche les verdicts (`ui/app.py`)
- **Mise en production** : `uvicorn gunicorn` (décidé ultérieurement)
- **Documentation** : plutôt des markdowns dans `docs/` ; un `README.md` à jour au niveau du projet

### 📚 Liaison avec la Documentation Professeur

- **Semaine 2** : Système d'entraînement (scikit-learn avec TF-IDF)
- **Semaine 3** : Exposition API FastAPI
- **Semaine 4** : Tests, contrainte d'entrée, abstention
- **Semaine 5** : Interface Streamlit, consommation par lot CSV
- **Semaines 9-10** : Mini-RAG et Agent Autonome (prochaine étape)

### 🔐 Modèle de données (schéma principal)

```json
{
  "label": "Hardware",
  "score": 0.92,
  "text": "Aperçu de la description analysée (100 caractères)",
  "status": "VALIDE"
}
```
