"""Wrapper de compatibilité : le Mini-RAG vit dans ``incidents_app.rag``.

Ce module conserve l'ancien chemin d'import (``from src.rag import MiniRAG``)
utilisé par les scripts et les tests. La source de vérité est le paquet
installable ``incidents_app``, conformément à l'architecture du projet.
"""

from __future__ import annotations

from incidents_app.rag import (
    DEFAULT_COLLECTION,
    DEFAULT_PERSIST_DIR,
    DEFAULT_RUNBOOKS_DIR,
    EMBEDDING_MODEL,
    ENV_RUNBOOKS,
    MiniRAG,
    main,
)

__all__ = [
    "DEFAULT_COLLECTION",
    "DEFAULT_PERSIST_DIR",
    "DEFAULT_RUNBOOKS_DIR",
    "EMBEDDING_MODEL",
    "ENV_RUNBOOKS",
    "MiniRAG",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
