"""Entraînement (TP Semaine 2) : classification multiclasse de tickets IT.

Usage (à adapter) :
  python src/train.py --csv data/all_tickets_processed_improved_v3.csv

Ce module fournit aussi une fonction testable : entrainer_sur_df().
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RACINE = Path(__file__).resolve().parents[1]
DATA_DIR = RACINE / "data"
MODELE_DEFAULT = RACINE / "models" / "incidents.joblib"
METRIQUES_DEFAULT = RACINE / "models" / "metrics.json"

SEUIL_F1 = 0.85
GRAINE = 42


@dataclass(frozen=True)
class EntreeData:
    x_col: str = "Document"
    y_col: str = "Topic_group"


def construire_pipeline(*, min_df: int = 2) -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=min_df, sublinear_tf=True)),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=GRAINE,
                ),
            ),
        ]
    )


def _valider_df(df: pd.DataFrame, *, cols: EntreeData) -> pd.DataFrame:
    if cols.x_col not in df.columns:
        raise ValueError(f"Colonne manquante : {cols.x_col}")
    if cols.y_col not in df.columns:
        raise ValueError(f"Colonne manquante : {cols.y_col}")

    df2 = df[[cols.x_col, cols.y_col]].copy()
    df2[cols.x_col] = df2[cols.x_col].astype(str)
    df2 = df2.dropna(subset=[cols.x_col, cols.y_col])
    df2 = df2[df2[cols.x_col].str.strip().astype(bool)]
    if df2.empty:
        raise ValueError("Dataset vide après nettoyage")
    return df2


def entrainer_sur_df(
    df: pd.DataFrame,
    *,
    modele_path: Path = MODELE_DEFAULT,
    metrics_path: Path = METRIQUES_DEFAULT,
    min_df: int = 2,
    test_size: float = 0.2,
    random_state: int = GRAINE,
    seed_strat: bool = True,
    seuil_f1: float = SEUIL_F1,
) -> dict[str, Any]:
    """Entraîne et sauvegarde le pipeline, puis écrit models/metrics.json.

    Retourne le dict de métriques.
    """

    cols = EntreeData()
    df2 = _valider_df(df, cols=cols)

    X = df2[cols.x_col]
    y = df2[cols.y_col].astype(str)

    # Découpage AVANT vectorisation
    stratify = y if seed_strat and y.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    pipeline = construire_pipeline(min_df=min_df)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    rapport = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0,
    )

    # Pour multiclass : macro avg F1
    f1_macro = float(rapport["macro avg"]["f1-score"])
    accuracy = float(rapport.get("accuracy", 0.0))

    modele_path = Path(modele_path)
    metrics_path = Path(metrics_path)
    modele_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, modele_path)

    payload = {
        "source": "dataframe",
        "date": date.today().isoformat(),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "f1_macro": round(f1_macro, 4),
        "accuracy": round(accuracy, 4),
        "seuil_f1": float(seuil_f1),
        "classes": sorted(map(str, getattr(pipeline, "classes_", []))),
    }

    metrics_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def charger_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=str, help="Chemin du CSV (data/all_tickets_processed_improved_v3.csv)")
    parser.add_argument("--modele", type=str, default=str(MODELE_DEFAULT))
    parser.add_argument("--metrics", type=str, default=str(METRIQUES_DEFAULT))
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=GRAINE)
    args = parser.parse_args()

    if not args.csv:
        raise SystemExit("--csv est requis")

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"CSV absent : {csv_path}")

    df = charger_csv(csv_path)

    payload = entrainer_sur_df(
        df,
        modele_path=Path(args.modele),
        metrics_path=Path(args.metrics),
        min_df=args.min_df,
        test_size=args.test_size,
        random_state=args.seed,
        seuil_f1=SEUIL_F1,
    )

    print(f"F1 macro : {payload['f1_macro']:.3f} (seuil {SEUIL_F1})")
    print(f"Modèle : {args.modele}")
    print(f"Métriques : {args.metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
