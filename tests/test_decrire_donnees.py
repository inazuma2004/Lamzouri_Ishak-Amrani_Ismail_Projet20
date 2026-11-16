"""Les chiffres de la fiche (rubrique 5) se recalculent : test sur l'échantillon versionné."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from decrire_donnees import ECHANTILLON, decrire


def test_echantillon_120_tickets_15_par_classe():
    d = decrire(pd.read_csv(ECHANTILLON))
    assert d["lignes"] == 120 and d["colonnes"] == 2 and d["doublons"] == 0
    assert len(d["classes"]) == 8 and set(d["classes"].values()) == {15}
    assert d["valeurs_manquantes"] == {"Document": 0, "Topic_group": 0}


def test_colonne_absente_refusee():
    with pytest.raises(ValueError, match="Topic_group"):
        decrire(pd.DataFrame({"Document": ["printer broken"]}))
