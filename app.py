import streamlit as st
import os

st.set_page_config(
    page_title="Détection de Fraude Bancaire",
    page_icon="🏦",
    layout="wide"
)

# =============================
# CSS
# =============================
st.markdown("""
<style>
.main-title{
    font-size:42px;
    color:#0B5394;
    font-weight:bold;
}
.subtitle{
    font-size:22px;
    color:#444;
}
.card{
    background-color:#F5F5F5;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:2px 2px 10px rgba(0,0,0,0.15);
}
.big{
    font-size:30px;
    color:#0B5394;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Logo
# =============================
col1,col2=st.columns([1,5])

with col1:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=120)

with col2:
    st.markdown("<p class='main-title'>Système Intelligent de Détection de Fraude Bancaire</p>",unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Projet de Machine Learning avec Streamlit</p>",unsafe_allow_html=True)

st.divider()

# =============================
# Image
# =============================
if os.path.exists("assets/banque.png"):
    st.image("assets/banque.png", use_container_width=True)

st.divider()

# =============================
# KPI
# =============================

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric("Transactions", "6 000")

with col2:
    st.metric("Fraudes détectées", "430")

with col3:
    st.metric("Accuracy", "86.44 %")

with col4:
    st.metric("Modèle", "Random Forest")

st.divider()

# =============================
# Présentation
# =============================

st.header("Présentation du projet")

st.write("""
Cette application permet de :

- Détecter automatiquement les transactions frauduleuses.
- Visualiser les statistiques du jeu de données.
- Analyser les performances du modèle de Machine Learning.
- Prédire le niveau de risque d'une nouvelle transaction.
""")

st.info("Utilisez le menu situé à gauche pour accéder aux différentes pages de l'application.")

st.divider()

st.header("Technologies utilisées")

c1,c2,c3,c4=st.columns(4)

with c1:
    st.success("Python")

with c2:
    st.success("Streamlit")

with c3:
    st.success("Scikit-Learn")

with c4:
    st.success("Pandas")

st.divider()

st.header("Navigation")

st.write("""
Le menu de gauche permet d'accéder à :

- Dashboard
- Analyse des données
- Prédiction
- Performance du modèle
- À propos
""")

st.success("Application développée dans le cadre d'un projet de Master en Intelligence Artificielle.")