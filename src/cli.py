"""Interface en ligne de commande : incidents --version, predict, serve."""

import sys

import click

from src.predict import ENV_MODELE, ModeleIntrouvable, charger_modele, predire

__version__ = "0.6.0"


@click.group()
@click.version_option(__version__, prog_name="incidents-app", message="%(prog)s %(version)s")
def main():
    """Classification automatique de tickets d'incidents IT."""


@main.command()
@click.argument("texte")
def predict(texte: str):
    """Affiche la categorie et le score pour un ticket."""
    try:
        modele = charger_modele()
    except ModeleIntrouvable as erreur:
        click.echo(f"Erreur : modele introuvable. Definissez {ENV_MODELE} ou lancez python src/train.py", err=True)
        sys.exit(1)
    resultat = predire(texte, modele)
    click.echo(f"{resultat['label']} {resultat['score']} [{resultat['status']}]")


@main.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
def serve(host: str, port: int):
    """Lance l'API FastAPI avec uvicorn."""
    import uvicorn
    uvicorn.run("app.main:app", host=host, port=port)
