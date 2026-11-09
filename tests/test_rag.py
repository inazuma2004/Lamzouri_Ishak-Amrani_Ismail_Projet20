"""Tests du Mini-RAG (Semaine 9).

Vérifie que la base vectorielle indexe les runbooks et retourne
des documents pertinents avec sources citées.
"""
from __future__ import annotations

import pytest

from src.rag import DEFAULT_RUNBOOKS_DIR, MiniRAG


@pytest.fixture
def rag():
    """Instance de MiniRAG avec runbooks indexés."""
    r = MiniRAG()
    r.indexer_runbooks(DEFAULT_RUNBOOKS_DIR)
    return r


def test_indexer_cree_base_vectorielle(rag):
    """L'indexation crée au moins un document par catégorie ML attendue."""
    assert rag.compter() >= 8  # 8 catégories ML + README


def test_indexer_categories_presentes(rag):
    """Toutes les catégories ML sont présentes dans la base."""
    attendu = {
        "Access",
        "Administrative rights",
        "HR Support",
        "Hardware",
        "Internal Project",
        "Miscellaneous",
        "Purchase",
        "Storage",
    }
    # Vérifier via une recherche sur chaque catégorie
    for categorie in attendu:
        resultats = rag.rechercher(categorie, categorie, k=1)
        assert len(resultats) >= 1, f"Aucun runbook pour la catégorie {categorie}"
        assert resultats[0]["categorie"] == categorie


def test_rechercher_retourne_source_citee(rag):
    """La recherche retourne un runbook avec chemin et score (source citable)."""
    resultats = rag.rechercher("Hardware", "ecran noir imprimante clavier", k=1)
    assert len(resultats) >= 1
    r = resultats[0]
    assert r.get("chemin")
    assert r.get("titre")
    assert "score" in r and 0.0 <= r["score"] <= 1.0
    assert "contenu" in r and len(r["contenu"]) > 0


def test_rechercher_hardware_retourne_runbook_hardware(rag):
    """Une requête Hardware retourne le runbook Hardware (pertinence thématique)."""
    resultats = rag.rechercher("Hardware", "imprimante papier bourre ecran", k=3)
    assert len(resultats) >= 1
    # Le premier résultat doit être Hardware (filtre where par catégorie)
    assert all(r["categorie"] == "Hardware" for r in resultats)


def test_rechercher_sans_resultat_quand_vide(monkeypatch, tmp_path):
    """Sans base indexée, la recherche retourne une liste vide."""
    r = MiniRAG(persist_directory=str(tmp_path / "chroma_vide"))
    # Pas d'indexation -> collection vide
    resultats = r.rechercher("Hardware", "ecran noir", k=3)
    assert resultats == []
