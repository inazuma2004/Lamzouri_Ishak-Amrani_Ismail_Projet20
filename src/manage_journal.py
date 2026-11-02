import json
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]

JOURNAL_PATH = RACINE / "docs" / "journal_temps_reel.md"

# Charge le journal s'il existe déjà ; sinon, initialise.
if JOURNAL_PATH.exists():
    with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
        try:
            journal = json.load(f)
        except json.JSONDecodeError:
            journal = []
else:
    journal = []

# Initialise un résumé simple (ici, juste un résumé structurel simple ; pas de traitement pour l'instant)
for entrée in journal:
    # Pour l'instant : simplement concaténer les événements pour remplir le fichier
    pass

# Si le fichier ne contient que le modèle vide, remplissez-le avec une structure.
if not journal:
    journal = {"contexte": "cadrage initial du projet", "TPs": [], "prochaines_étapes": []}
    with open(JOURNAL_PATH, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2, ensure_ascii=False)

print(f"Journal d'exécution actualisé à {JOURNAL_PATH}")
