# Architecture

```mermaid
flowchart TD
    U["Technicien du helpdesk"] -->|ticket ou fichier CSV| UI["Interface web React (web/), servie par l'API sur /"]
    U -->|ligne de commande| CLI["Commande incidents (incidents_app/cli.py)"]
    UI -->|HTTP, clé X-API-Key| API["API FastAPI (app/) : /v1/predict, /v1/resolve, /v1/search"]
    API --> Q
    CLI --> Q
    subgraph Equipe ["Équipe d'agents (incidents_app/equipe.py)"]
        Q["Qualificateur : TF-IDF + régression logistique ; sous 0,60 : A_VERIFIER"]
        P["Priorisateur : règles P1 à P4"]
        D["Documentaliste : recherche dans les runbooks ; sous 0,27 : aucune source"]
        R["Rédacteur : réponse construite à partir des passages"]
        V["Vérificateur : source citée, escalade, injection"]
        Q --> P --> D --> R --> V
        V -->|à corriger, 3 itérations au plus| R
    end
    D --- RB[("data/runbooks : 8 runbooks, 27 sections")]
    V -->|catégorie, priorité, procédure citée, statut| API
```

| Composant | Dossier | Push |
| --- | --- | --- |
| Commande `incidents` | `incidents_app/cli.py` | S1-4 (squelette), S2-1 (`predict`) |
| Modèle et prédiction | `src/train.py`, `incidents_app/predict.py` | S2-1 |
| Jeu d'or et évaluation | `tests/jeu_or.csv`, `src/evaluate.py` | S2-2 |
| API | `app/` | S2-3 |
| Interface web (React, Vite, TypeScript, Tailwind CSS) | `web/` | S2-4 |
| Runbooks, recherche, équipe d'agents | `data/runbooks/`, `incidents_app/` | S2-1 à S3-1 |
| Docker, installateur | `docker/`, `installateur/` | S3-3 |
