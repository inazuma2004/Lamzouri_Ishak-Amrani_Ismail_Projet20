# CONTEXTE DU PROJET : IT Incident Classification (incidentsIT)

## État Global
- **Binôme** : Lamzouri Ishak, Amrani Ismail
- **Dépôt** : https://github.com/inazuma2004/Lamzouri_Ishak-Amrani_Ismail_Projet20
- **Version** : 0.1.0
- **Dernière mise à jour** : 2026-10-28

## Architecture (Conforme TP1-TP11)
- `src/` : Logique métier (train.py, predict.py)
- `app/` : API FastAPI
- `ui/` : Interface Streamlit
- `tests/` : Suite de tests (pytest)
- `models/` : Modèles (incidents.joblib)
- `data/` : Dataset Kaggle
- `docs/` : Journal de bord et documentation

## Pipeline MLOps
- **Modèle** : TF-IDF + LogisticRegression
- **Performance** : F1-macro 0.857
- **CI/CD** : GitHub Actions (Ruff, Pytest, Mypy)

## Roadmap (Roadmap Académique)
- [x] Semaine 2-5 : Core pipeline, API, UI, Tests (OK)
- [ ] Semaine 6 : Dockerisation & Déploiement
- [ ] Semaine 9-10 : Mini-RAG & Agent Autonome

## Notes de Rigueur Académique
- Utiliser `pyproject.toml` pour le packaging.
- Ne jamais versionner `.joblib` ou `.csv` (Gitignore configuré).
- Chaque PR doit être validée par le binôme.
- Consigner systématiquement les erreurs de prédiction dans `docs/journal_tp1_tp5.md`.

## Prochaine Action
- Continuer le développement suivant les consignes du cours (TP6 et suivants).
