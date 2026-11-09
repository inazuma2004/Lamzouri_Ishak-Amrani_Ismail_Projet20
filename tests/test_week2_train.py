import json
from pathlib import Path

import pandas as pd
import pytest


def test_train_and_predict_from_dataframe(tmp_path: Path):
    # Import doit exister : src/train.py et src/predict.py seront créés (TP2)
    from src.predict import predict
    from src.train import entrainer_sur_df

    df = pd.DataFrame(
        [
            {"Document": "vpn login access denied", "Topic_group": "Access"},
            {"Document": "cannot connect to internal vpn", "Topic_group": "Access"},
            {"Document": "password reset request", "Topic_group": "Access"},
            {"Document": "disk is full storage capacity", "Topic_group": "Storage"},
            {"Document": "low disk space on server", "Topic_group": "Storage"},
            {"Document": "unable to access shared folder", "Topic_group": "Storage"},
            {"Document": "need new license purchase", "Topic_group": "Purchase"},
            {"Document": "software license renewal", "Topic_group": "Purchase"},
            {"Document": "buy new workstation", "Topic_group": "Purchase"},
        ]
    )

    modele_path = tmp_path / "incidents.joblib"
    metrics_path = tmp_path / "metrics.json"

    entrainer_sur_df(
        df,
        modele_path=modele_path,
        metrics_path=metrics_path,
        min_df=1,
        test_size=0.33,
        random_state=42,
    )

    assert modele_path.exists()
    assert metrics_path.exists()

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    for key in ["f1_macro", "accuracy", "n_train", "n_test", "seuil_f1"]:
        assert key in payload

    out = predict("cannot connect vpn", modele_path=modele_path)
    # Le seuil d'abstention (0.60) peut renvoyer INDETERMINE si le modèle n'est pas confiant
    # sur ce petit jeu d'entraînement : c'est un comportement attendu et cohérent.
    assert out["label"] in {"Access", "Storage", "Purchase", "INDETERMINE"}
    assert 0.0 <= out["score"] <= 1.0
    assert out["status"] in {"VALIDE", "A_VERIFIER"}
    # Cohérence : label INDETERMINE <=> status A_VERIFIER, sinon VALIDE
    if out["label"] == "INDETERMINE":
        assert out["status"] == "A_VERIFIER"
        assert out["score"] < 0.60
    else:
        assert out["status"] == "VALIDE"
        assert out["score"] >= 0.60

    # Texte vide doit être refusé
    with pytest.raises(ValueError):
        predict("   ", modele_path=modele_path)
