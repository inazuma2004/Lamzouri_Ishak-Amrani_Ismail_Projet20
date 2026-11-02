from datetime import datetime

# Journal d'exécution initial (pour le tournage des TP)
JOURNAL_PATH = "docs/journal_temps_reel.md"

# Assurez-vous que le dossier parent existe avant d'écrire
import os

os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)

def enregistrer(event: str, details: dict | None = None) -> None:
    """Ajoute une entrée timestampée au journal d'exécution.
    Adapté à la granularité du cours : chaque appel d'outil et chaque test
    doit être enregistré avec le nom du fichier, la ligne et un contexte court.
    """
    details = details or {}
    entry = {
        "horodatage": datetime.now(tz=__import__("datetime").timezone.utc).isoformat(),
        "event": event,
        "details": details,
    }
    import json
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(entry)
    with open(JOURNAL_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Initialisez le journal avec une entrée d'événement de démarrage (simplifiée pour l'instant)
enregistrer("démarrage", {"action": "initialiser le journal d'exécution"})
print(f"Journal d'exécution actualisé à {JOURNAL_PATH}")
