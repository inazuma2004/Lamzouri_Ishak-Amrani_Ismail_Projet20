"""Tests de l'interface en ligne de commande (CLI) `incidents`.

Couvre : `incidents --version`, `incidents predict` (succès + modèle introuvable).
"""
from __future__ import annotations

from click.testing import CliRunner

from incidents_app.cli import main


def test_cli_version():
    """La commande --version affiche incidents-app 0.6.0."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "incidents-app 1.0.0" in result.output


def test_cli_predict_sans_modele(monkeypatch, tmp_path):
    """Sans modèle disponible, incidents predict quitte avec code 1 et message d'erreur."""
    runner = CliRunner()
    # Forcer le chemin du modèle vers un fichier inexistant
    monkeypatch.setenv("INCIDENTS_MODELE", str(tmp_path / "inexistant.joblib"))
    result = runner.invoke(main, ["predict", "Impossible de se connecter au VPN"])
    assert result.exit_code == 1
    assert "modèle introuvable" in result.output.lower() or "introuvable" in result.output.lower()
