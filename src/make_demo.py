import json
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
DATA_DIR = RACINE / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_DEMO = DATA_DIR / "demo_reviews.csv"

# Simulez une classification d'incidents IT (4 catégories, comme dans la vraie donnée)
DATA = {
    "Document": [
        "vpn login access denied",
        "cannot connect to internal vpn",
        "password reset request",
        "disk is full storage capacity",
        "low disk space on server",
        "unable to access shared folder",
        "need new license purchase",
        "software license renewal",
        "buy new workstation",
        "screen flickering display broken",
        "keyboard not responding",
        "mouse scroll not working",
        "printer out of ink",
        "wifi connection unstable",
        "email server cannot receive",
        "outlook not opening attachment",
        "server downtime scheduled",
        "database connection timeout",
        "backup failed",
        "security scan required",
    ],
    "Topic_group": [
        "Access",
        "Access",
        "Access",
        "Storage",
        "Storage",
        "Storage",
        "Purchase",
        "Purchase",
        "Purchase",
        "Hardware",
        "Hardware",
        "Hardware",
        "Hardware",
        "Access",
        "Access",
        "Access",
        "Access",
        "Access",
        "Access",
        "Access",
    ],
}

if not CSV_DEMO.exists():
    df = pd.DataFrame(DATA)
    df.to_csv(CSV_DEMO, index=False)
    print(f"Created demo dataset at {CSV_DEMO}")
else:
    df = pd.read_csv(CSV_DEMO)
    print(f"Demo dataset already exists at {CSV_DEMO} ({len(df)} lignes)")

METRICS_FILE = RACINE / "models" / "metrics_demo.json"
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

if METRICS_FILE.exists():
    print(f"Métriques démo déjà sauvegardées à {METRICS_FILE}")
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    print("Métriques :\n" + json.dumps(metrics, indent=2, ensure_ascii=False))
    sys.exit(0)

# Entraînez un modèle très petit pour la démo
from src.train import entrainer_sur_df

payload = entrainer_sur_df(
    df,
    modele_path=RACINE / "models" / "incidents_demo.joblib",
    metrics_path=METRICS_FILE,
    min_df=1,
    test_size=0.3,
    random_state=42,
    seuil_f1=0.0,
)

print("\nMétriques démo :\n" + json.dumps(payload, indent=2, ensure_ascii=False))
print(f"\nDataset démo prêt : {CSV_DEMO}")
