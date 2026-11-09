"""Pont entre l'API FastAPI et le paquet incidents_app.

Aucune manipulation de sys.path : l'API importe le paquet comme n'importe quelle dependance.
"""

from incidents_app.predict import charger_modele, predire


class IncidentClassifier:
    """Enveloppe le modele d'incidents pour l'API."""

    model_name = "tfidf-logreg (TP2, models/incidents.joblib)"

    def __init__(self) -> None:
        self.pipeline = charger_modele()

    def predict(self, text: str) -> dict:
        """Predit la categorie et gere le seuil d'incertitude."""
        return predire(text, modele=self.pipeline)


def load_model() -> IncidentClassifier:
    """Charge le modele une fois, au demarrage de l'API."""
    return IncidentClassifier()
