"""Tests du paquet INSTALLÉ : lancés hors du dossier source, ils échouent si la roue est incomplète."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Ces tests visent le paquet INSTALLÉ. Dans le dépôt, l'API ajoute src/ au chemin d'import :
# incidents_app y serait trouvé dans les sources, ce qui ne prouve rien. On les ignore donc,
# sauf quand scripts/verifier_livrable.py les lance (VERIFICATION_LIVRABLE=1) : là, ils doivent passer.
_spec = importlib.util.find_spec("incidents_app")
if not (_spec and "site-packages" in (_spec.origin or "")) and not os.environ.get("VERIFICATION_LIVRABLE"):
    pytest.skip("paquet non installé : python scripts/verifier_livrable.py", allow_module_level=True)

import incidents_app  # noqa: E402

# La commande est installée à côté de l'interpréteur qui lance les tests (bin/ sous Linux, Scripts sous Windows).
# On ne compte pas sur le PATH : il dépend de l'activation de l'environnement.
COMMANDE = shutil.which("incidents", path=str(Path(sys.executable).parent))


def test_importe_depuis_le_paquet_installe():
    assert "site-packages" in incidents_app.__file__, "le test lit les sources, pas la roue installée"


def test_version_lue_dans_les_metadonnees():
    assert incidents_app.__version__ == "1.0.0"


def test_modele_embarque_dans_la_roue():
    # Le modèle embarqué dans la roue permet de prédire sans INCIDENTS_MODELE.
    assert incidents_app.predict("cannot login vpn password expired")["label"] == "Access"


def test_texte_vide_refuse():
    with pytest.raises(ValueError):
        incidents_app.predict("   ")


def test_commande_installee():
    assert COMMANDE, "commande incidents introuvable à côté de l'interpréteur"
    sortie = subprocess.run([COMMANDE, "predict", "cannot login vpn password expired"],
                            capture_output=True, text=True, check=True).stdout
    assert json.loads(sortie)["label"] == "Access"


def test_commande_code_retour_sur_erreur():
    assert COMMANDE, "commande incidents introuvable à côté de l'interpréteur"
    assert subprocess.run([COMMANDE, "predict"], capture_output=True, check=False).returncode != 0
