"""Deux graphiques pour l'onglet traitement par lot (TP 3).

Répartition des catégories prédites et distribution des scores de confiance.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


def graphiques(resultats: list[dict]) -> None:
    """Affiche deux bar_chart à partir des résultats d'un lot de tickets.

    Chaque résultat est un dict avec au moins les clés `label`, `score`, `statut`.
    """
    if not resultats:
        st.info("Aucun résultat à afficher.")
        return

    df = pd.DataFrame(resultats)

    st.subheader("Répartition des catégories prédites")
    counts = df["label"].value_counts().sort_index()
    st.bar_chart(counts)

    st.subheader("Distribution de la confiance")
    tranches = pd.cut(
        df["score"],
        bins=[0.0, 0.6, 0.7, 0.8, 0.9, 1.0],
        labels=["0,0 à 0,6", "0,6 à 0,7", "0,7 à 0,8", "0,8 à 0,9", "0,9 à 1,0"],
    )
    st.bar_chart(tranches.value_counts().sort_index())
    st.caption("Sous 0,60 : ticket renvoyé à un opérateur humain (statut A_VERIFIER).")
