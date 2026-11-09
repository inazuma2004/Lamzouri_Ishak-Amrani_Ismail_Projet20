"""Interface Streamlit (TP5 + S9-S10) : elle appelle l'API, jamais le modèle.

Lancer, API déjà démarrée dans un autre terminal : streamlit run ui/app.py
"""
import io

import pandas as pd
import streamlit as st

from ui import client
from ui.graphiques_demo import graphiques

st.set_page_config(page_title="Incidents IT - Agent Autonome", page_icon="🤖")
st.title("🤖 Agent Autonome de Résolution d'Incidents IT")
st.caption("Classification ML + Résolution RAG — Conforme à l'architecture M. Larhlimi")
st.caption(
    "ℹ️ Le modèle ML a été entraîné sur des tickets en anglais : "
    "décrivez l'incident en anglais pour une meilleure confiance. "
    "Sous 60 %, l'agent renvoie vers un opérateur humain."
)

session = client.creer_session()

onglet_classif, onglet_agent, onglet_batch = st.tabs(
    ["🔍 Classification (ML)", "🧠 Résolution agentique (ML + RAG)", "📁 Traitement par lot CSV"]
)

# ---------------------------------------------------------------------------
# Onglet 1 : Classification pure (modèle ML seulement)
# ---------------------------------------------------------------------------
with onglet_classif:
    st.subheader("Classifier un incident (modèle ML supervisé)")
    texte = st.text_area("Description de l'incident", key="classif_texte")
    if st.button("Analyser", key="classif_btn"):
        if not texte.strip():
            st.warning("Veuillez saisir une description d'incident.")
        else:
            reponse = client.predire(session, texte)
            if reponse.ok:
                badge = "✅" if reponse.statut == "VALIDE" else "⚠️"
                st.success(f"{badge} Catégorie : {reponse.label} (confiance: {reponse.score:.2%})")
                st.info(f"Statut : {reponse.statut}")
                if reponse.statut == "A_VERIFIER":
                    st.warning(
                        "Confiance sous le seuil d'abstention (60%). "
                        "Un opérateur humain doit valider avant toute action."
                    )
            else:
                st.error(reponse.message)

# ---------------------------------------------------------------------------
# Onglet 2 : Résolution agentique (ML + RAG)
# ---------------------------------------------------------------------------
with onglet_agent:
    st.subheader("Résolution autonome (qualification ML + runbook RAG)")
    texte_agent = st.text_area("Description de l'incident", key="agent_texte")
    if st.button("Résoudre", key="agent_btn"):
        if not texte_agent.strip():
            st.warning("Veuillez saisir une description d'incident.")
        else:
            reponse = client.resoudre(session, texte_agent)
            if reponse.ok:
                if reponse.action_humaine:
                    st.error("🛑 Intervention humaine requise")
                    st.info(f"Statut : {reponse.statut}")
                    st.write(reponse.message_humain or "Aucune précision.")
                else:
                    st.success("✅ Résolution proposée par l'agent autonome")
                    st.info(f"Catégorie : {reponse.label} (confiance: {reponse.score:.2%})")
                    st.info(f"Statut : {reponse.statut}")
                    if reponse.runbook:
                        st.subheader(f"📖 Procédure : {reponse.runbook}")
                        st.markdown(reponse.resolution or "Procédure non disponible.")
                    if reponse.sources:
                        st.subheader("📚 Sources citées (RAG)")
                        for src in reponse.sources:
                            st.caption(
                                f"• {src.get('titre', 'Runbook')} — "
                                f"{src.get('chemin', 'inconnu')} (score {src.get('score', 0):.2f})"
                            )
            else:
                st.error(reponse.message)

# ---------------------------------------------------------------------------
# Onglet 3 : Traitement par lot (CSV)
# ---------------------------------------------------------------------------
with onglet_batch:
    st.subheader("Traitement par lot d'incidents (fichier CSV)")
    st.caption("Colonne attendue dans le CSV : `Document` (texte de l'incident).")
    fichier = st.file_uploader("Déposez un fichier CSV de tickets", type=["csv"], key="batch_uploader")
    if fichier is not None:
        try:
            df_entree = pd.read_csv(fichier)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Impossible de lire le fichier CSV : {exc}")
            st.stop()
        if "Document" not in df_entree.columns:
            st.error("Le CSV doit contenir une colonne nommée 'Document'.")
            st.stop()

        textes = df_entree["Document"].dropna().astype(str).tolist()
        if not textes:
            st.warning("Aucun ticket à traiter dans ce fichier.")
            st.stop()

        with st.spinner(f"Analyse de {len(textes)} ticket(s) en cours..."):
            reponses = client.predire_lot(session, textes)

        resultats = []
        for texte, rep in zip(textes, reponses):
            resultats.append(
                {
                    "Document": texte,
                    "Catégorie": rep.label if rep.ok else "ERREUR",
                    "Score": f"{rep.score:.2%}" if rep.ok and rep.score is not None else "-",
                    "Statut": rep.statut if rep.ok else "REFUS",
                    "Message": rep.message if not rep.ok else "",
                }
            )

        df_resultats = pd.DataFrame(resultats)
        st.success(f"{len(textes)} ticket(s) traité(s).")
        st.dataframe(df_resultats, use_container_width=True, hide_index=True)

        graphiques([{"label": r["Catégorie"], "score": (float(r["Score"].rstrip("%")) / 100) if r["Score"] != "-" else 0.0, "statut": r["Statut"]} for r in resultats])

        resume = client.resumer(reponses)
        st.subheader("Résumé")
        for cle, valeur in resume.items():
            st.metric(cle, valeur)

        buffer = io.StringIO()
        df_resultats.to_csv(buffer, index=False, encoding="utf-8")
        st.download_button(
            label="⬇️ Télécharger le CSV annoté",
            data=buffer.getvalue(),
            file_name="tickets_annotes.csv",
            mime="text/csv",
        )

