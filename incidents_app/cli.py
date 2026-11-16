"""Commande `incidents` : point d'entrée de l'application.

Squelette de la semaine 1 : --version et --help. Les sous-commandes arrivent avec le cœur du
projet (predict au push S2-1, serve et ui aux push S2-3 et S2-4).
"""

import click

from incidents_app import __version__


@click.group()
@click.version_option(__version__, prog_name="incidents-app", message="%(prog)s %(version)s")
def main():
    """Agent de résolution d'incidents IT."""
