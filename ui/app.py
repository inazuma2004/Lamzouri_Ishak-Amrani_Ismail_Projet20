
import streamlit as st

from ui import client

st.set_page_config(page_title="Incidents IT Classifier")
st.title("Classification d'Incidents IT")

session = client.creer_session()
texte = st.text_area("Description de l'incident")

if st.button("Analyser"):
    reponse = client.predire(session, texte)
    if reponse.ok:
        st.success(f"Catégorie : {reponse.label} (confiance: {reponse.score:.2%})")
    else:
        st.error(reponse.message)
