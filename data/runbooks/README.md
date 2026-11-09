# Runbooks IT — Base de connaissances Mini-RAG

Ce dossier contient les procédures de dépannage (runbooks) par catégorie d'incident IT.
Chaque fichier Markdown correspond à une catégorie exacte du modèle ML de classification :

| Fichier | Catégorie ML | Contenu |
|---------|--------------|---------|
| `Hardware.md` | Hardware | Écran, clavier, imprimante, périphériques |
| `Access.md` | Access | VPN, mot de passe, compte verrouillé, authentification |
| `Storage.md` | Storage | Disque plein, quota, sauvegarde, stockage réseau |
| `Purchase.md` | Purchase | Licence logicielle, poste de travail, achat matériel |
| `HR Support.md` | HR Support | Congés, onboarding, droits administratifs RH |
| `Internal Project.md` | Internal Project | Suivi de projet, jalon, reporting interne |
| `Miscellaneous.md` | Miscellaneous | Demandes diverses non classées ailleurs |
| `Administrative rights.md` | Administrative rights | Élévation de privilèges, installation de logiciels |

## Méthode d'indexation (Mini-RAG)

Le script `scripts/indexer_runbooks.py` lit chaque fichier `.md`, calcule les embeddings via `sentence-transformers`, et stocke les vecteurs dans une base locale `chroma_db/`.

Lorsqu'un ticket est qualifié par le modèle ML (ex: `Hardware`), l'agent interroge le RAG avec la catégorie pour récupérer le runbook correspondant et les procédures de dépannage associées.

## Règles

- Les runbooks sont des **documents source citables** (approche RAG, pas de génératif seul).
- L'agent cite toujours la source du runbook utilisé.
- Aucun donnée personnelle réelle (RGPD, loi 09-08) : uniquement des procédures génériques.
