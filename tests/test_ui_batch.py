"""Tests du traitement par lot CSV (TP 3) sur le client UI."""
from ui import client


def test_resumer_compte_par_categorie_statut():
    reponses = [
        client.Reponse(True, label="Access", score=0.9, statut="VALIDE"),
        client.Reponse(True, label="Hardware", score=0.8, statut="VALIDE"),
        client.Reponse(True, label="Access", score=0.5, statut="A_VERIFIER"),
        client.Reponse(False, message="Erreur API"),
    ]
    resume = client.resumer(reponses)
    assert resume["Access (VALIDE)"] == 1
    assert resume["Access (A_VERIFIER)"] == 1
    assert resume["Hardware (VALIDE)"] == 1
    assert resume["REFUS OU ERREUR"] == 1


def test_predire_lot_retourne_autant_de_reponses_que_de_textes(monkeypatch):
    def faux_predire(session, texte):
        return client.Reponse(True, label="Access", score=0.9, statut="VALIDE")

    monkeypatch.setattr(client, "predire", faux_predire)
    session = object()
    reponses = client.predire_lot(session, ["ticket 1", "ticket 2", "ticket 3"])  # type: ignore[arg-type]
    assert len(reponses) == 3
    assert all(r.ok for r in reponses)
