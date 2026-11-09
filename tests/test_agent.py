"""Tests de l'IA Agentique (Semaine 10).

Vérifie que l'agent :
- qualifie via ML,
- respecte le seuil d'abstention (A_VERIFIER si score < 0.60),
- résout via RAG avec sources citées quand la confiance est suffisante,
- ne fait jamais de génératif seul (toujours une source de runbook).
"""
from __future__ import annotations

import pytest

from src.agent import IncidentAgent
from src.rag import DEFAULT_RUNBOOKS_DIR, MiniRAG


@pytest.fixture
def agent():
    a = IncidentAgent(rag=MiniRAG())
    a.rag.indexer_runbooks(DEFAULT_RUNBOOKS_DIR)
    return a


def test_agent_resout_ticket_clair(agent):
    """Un ticket clair (Access, haute confiance) est résolu avec runbook + source."""
    texte = "cannot login vpn password expired please reset account locked"
    resultat = agent.resoudre(texte)
    assert resultat["statut"] == "VALIDE"
    assert resultat["categorie"] == "Access"
    assert resultat["score"] >= 0.60
    assert resultat["action_humaine"] is False
    assert resultat["runbook"] is not None
    assert "Access" in resultat["runbook"]
    assert len(resultat["sources"]) >= 1
    assert resultat["sources"][0]["chemin"]  # source citée
    assert "mot de passe" in resultat["resolution"].lower() or "vpn" in resultat["resolution"].lower()


def test_agent_abstention_sous_seuil(agent):
    """Un texte ambigu donne A_VERIFIER et pas de résolution automatique."""
    texte = "xqzvb wlkptr grombu"
    resultat = agent.resoudre(texte)
    assert resultat["statut"] == "A_VERIFIER"
    assert resultat["action_humaine"] is True
    assert resultat["runbook"] is None
    assert resultat["sources"] == []
    assert "humain" in resultat["resolution"].lower()


def test_agent_toujours_source_citee_quando_valide(agent):
    """Quand le statut est VALIDE, une source de runbook est toujours citée (pas de génératif seul)."""
    texte = "server disk full storage quota exceeded backup failed"
    resultat = agent.resoudre(texte)
    if resultat["statut"] == "VALIDE":
        assert len(resultat["sources"]) >= 1
        assert resultat["runbook"] is not None
        assert resultat["action_humaine"] is False


def test_agent_qualifier_retourne_categorie_score_statut(agent):
    """qualifier() retourne categorie, score et statut cohérents."""
    texte = "need new license purchase for new employee"
    qual = agent.qualifier(texte)
    assert "categorie" in qual
    assert "score" in qual
    assert "statut" in qual
    assert qual["statut"] in {"VALIDE", "A_VERIFIER"}
    assert 0.0 <= qual["score"] <= 1.0
