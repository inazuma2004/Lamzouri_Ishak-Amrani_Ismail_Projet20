"""Wrapper de compatibilité : l'agent vit dans ``incidents_app.agent``.

Ce module conserve l'ancien chemin d'import (``from src.agent import
IncidentAgent``). La source de vérité est le paquet installable
``incidents_app``.
"""

from __future__ import annotations

from incidents_app.agent import (
    STATUT_A_VERIFIER,
    STATUT_VALIDE,
    IncidentAgent,
    main,
)

__all__ = [
    "STATUT_A_VERIFIER",
    "STATUT_VALIDE",
    "IncidentAgent",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
