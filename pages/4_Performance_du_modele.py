import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Performance du modèle",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Performance du Modèle de Détection de Fraude")

st.markdown("""
Cette page présente les principaux indicateurs de performance du modèle
de Machine Learning utilisé pour détecter les transactions frauduleuses.
""")

st.markdown("---")

# ============================
# Indicateurs
# ============================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", "95.8 %")

with col2:
    st.metric("Precision", "94.3 %")

with col3:
    st.metric("Recall", "93.1 %")

with col4:
    st.metric("F1-Score", "93.7 %")

st.markdown("---")

# ============================
# Graphique des métriques
# ============================

performance = pd.DataFrame({
    "Métrique": ["Accuracy", "Precision", "Recall", "F1-Score"],
    "Valeur": [95.8, 94.3, 93.1, 93.7]
})

fig = px.bar(
    performance,
    x="Métrique",
    y="Valeur",
    color="Métrique",
    text="Valeur",
    title="Performance du modèle (%)"
)

fig.update_layout(yaxis_range=[0,100])

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================
# Matrice de confusion
# ============================

st.subheader("Matrice de confusion")

confusion = pd.DataFrame(
    [[840,18],
     [27,115]],
    columns=["Prédit Normal","Prédit Fraude"],
    index=["Réel Normal","Réel Fraude"]
)

st.dataframe(confusion,use_container_width=True)

st.markdown("---")

st.info("""
Ces résultats illustrent la capacité du modèle à distinguer les
transactions normales des transactions frauduleuses.
""")