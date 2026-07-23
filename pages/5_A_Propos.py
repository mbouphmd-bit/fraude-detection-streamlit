import streamlit as st

st.set_page_config(
    page_title="À propos",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ À propos du projet")

st.markdown("---")

st.header("🎯 Objectif du projet")

st.write("""
Cette application a été développée dans le cadre d'un projet de Machine Learning.
Elle permet d'analyser des transactions bancaires et d'identifier les opérations
susceptibles d'être frauduleuses grâce à un modèle d'intelligence artificielle.
""")

st.markdown("---")

st.header("⚙️ Fonctionnalités")

st.markdown("""
- 🏠 Page d'accueil
- 📊 Dashboard interactif
- 📈 Analyse des données
- 🤖 Prédiction d'une transaction
- 📉 Performance du modèle
- ℹ️ Présentation du projet
""")

st.markdown("---")

st.header("🛠️ Technologies utilisées")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
    """)

with col2:
    st.markdown("""
- Plotly
- Joblib
- VS Code
- GitHub
    """)

st.markdown("---")

st.header("🗂️ Jeu de données")

st.write("""
Le modèle a été entraîné sur un jeu de données contenant des transactions bancaires.
Chaque transaction comprend notamment :

- Type de transaction
- Statut de l'opération
- Localisation
- Montant
- Date
- Classe de la transaction (Normale, Suspecte ou Fraude)
""")

st.markdown("---")

st.header("🤖 Modèle de Machine Learning")

st.write("""
Le modèle de classification a été entraîné afin de détecter automatiquement
les transactions frauduleuses.

Les données ont été prétraitées avant l'entraînement :

- Nettoyage des données
- Encodage des variables catégorielles
- Standardisation des variables numériques
- Entraînement du modèle
- Sauvegarde avec Joblib
""")

st.markdown("---")

st.header("👨‍🎓 Auteur")

st.write("""
**Projet réalisé dans le cadre du Master Intelligence Artificielle (DIT).**

Cette application illustre l'utilisation du Machine Learning pour améliorer
la détection de fraude bancaire et faciliter l'analyse des transactions.
""")

st.markdown("---")

st.success("✅ Merci d'avoir utilisé cette application.")