import urllib.parse
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA_DIR = RACINE / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

KAGGLE_DATASET = "adisongoh/it-service-ticket-classification-dataset"
KAGGLE_FILE = "all_tickets_processed_improved_v3.csv"
URL_KAGGLE = f"https://www.kaggle.com/datasets/{urllib.parse.quote(KAGGLE_DATASET)}/{urllib.parse.quote(KAGGLE_FILE)}"

CSV_OUTPUT = DATA_DIR / KAGGLE_FILE

# Si le CSV n'existe pas, essayons de le télécharger depuis Kaggle (l'API Kaggle n'est pas disponible ; utiliser requests HTTP direct si autorisé)
if not CSV_OUTPUT.exists():
    print(f"CSV Kaggle manquant : {CSV_OUTPUT}")
    print("Nous allons générer un CSV de démarrage à la place.")
    # Utilisez le fichier de démarrage généré précédemment (data/demo_reviews.csv) pour les tests et la démonstration
    from src.make_demo import CSV_DEMO
    if CSV_DEMO.exists():
        df = pd.read_csv(CSV_DEMO)
        df.to_csv(CSV_OUTPUT, index=False)
        print(f"Dataset de démo copié vers : {CSV_OUTPUT} ({len(df)} lignes)")
    else:
        print(f"Dataset de démo manquant à {CSV_DEMO}. Exécutez `python src/make_demo.py` pour générer les données de démonstration.")
else:
    print(f"Dataset Kaggle déjà présent : {CSV_OUTPUT} ({CSV_OUTPUT.stat().st_size} octets)")
