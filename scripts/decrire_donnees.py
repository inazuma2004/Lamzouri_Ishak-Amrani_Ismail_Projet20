"""Recalcule les chiffres du jeu de données cités dans la fiche de suivi (rubrique 5).

Usage :
    python scripts/decrire_donnees.py                                        # échantillon du dépôt
    python scripts/decrire_donnees.py data/all_tickets_processed_improved_v3.csv   # jeu complet
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

ECHANTILLON = Path(__file__).resolve().parents[1] / "data" / "sample" / "tickets_sample.csv"
COLONNES = ("Document", "Topic_group")


def decrire(df: pd.DataFrame) -> dict[str, Any]:
    manquantes = [c for c in COLONNES if c not in df.columns]
    if manquantes:
        raise ValueError(f"colonnes absentes : {manquantes} (attendu : {list(COLONNES)})")
    mots = df["Document"].fillna("").astype(str).str.split().str.len()
    return {
        "lignes": len(df),
        "colonnes": df.shape[1],
        "valeurs_manquantes": {c: int(df[c].isna().sum()) for c in df.columns},
        "doublons": int(df.duplicated().sum()),
        "classes": {str(k): int(v) for k, v in df["Topic_group"].value_counts().items()},
        "mots_par_ticket": {"moyenne": round(float(mots.mean()), 1), "mediane": float(mots.median()),
                            "min": int(mots.min()), "max": int(mots.max())},
    }


def main() -> int:
    chemin = Path(sys.argv[1]) if len(sys.argv) > 1 else ECHANTILLON
    d = decrire(pd.read_csv(chemin))
    print(f"{chemin.name} : {d['lignes']} lignes, {d['colonnes']} colonnes, {d['doublons']} doublons")
    print(f"valeurs manquantes : {d['valeurs_manquantes']}")
    m = d["mots_par_ticket"]
    print(f"mots par ticket : moyenne {m['moyenne']}, médiane {m['mediane']}, min {m['min']}, max {m['max']}")
    for classe, n in d["classes"].items():
        print(f"  {classe:<22} {n:>6}  {n / d['lignes']:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
