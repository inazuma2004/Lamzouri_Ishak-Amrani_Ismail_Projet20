"""Premier test : le point d'entrée se lance et annonce sa version."""
import subprocess
import sys

from click.testing import CliRunner

from incidents_app import __version__
from incidents_app.cli import main


def test_version():
    r = CliRunner().invoke(main, ["--version"])
    assert r.exit_code == 0 and r.output.strip() == f"incidents-app {__version__}"


def test_lance_comme_module():
    r = subprocess.run([sys.executable, "-m", "incidents_app", "--help"], capture_output=True, text=True, check=False)
    assert r.returncode == 0 and "Agent de résolution d'incidents IT" in r.stdout
