"""Script d'indexation des runbooks IT dans la base vectorielle Mini-RAG (Semaine 9).

Usage :
    python scripts/indexer_runbooks.py

Produit : dossier chroma_db/ contenant la base vectorielle (exclu de Git).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Importer depuis le dépôt (équivalent à `pip install -e .`)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from incidents_app.rag import DEFAULT_RUNBOOKS_DIR, MiniRAG


def main() -> int:
    rag = MiniRAG()
    resultats = rag.indexer_runbooks(DEFAULT_RUNBOOKS_DIR)
    if not resultats:
        print("Aucun runbook trouvé à indexer.")
        return 1
    print(f"Runbooks indexés : {len(resultats)}")
    for categorie in sorted(resultats):
        print(f"  - {categorie}")
    print(f"Total documents dans la base : {rag.compter()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
