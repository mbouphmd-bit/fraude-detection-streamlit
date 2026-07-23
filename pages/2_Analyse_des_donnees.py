import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Analyse des données",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CHARGEMENT DES DONNÉES
# ==========================================================

@st.cache_data
def charger_donnees():

    df = pd.read_csv(
        "data/Bank_transaction_scenario1.csv",
        sep=";"
    )

    df["Date"] = pd.to_datetime(df["Date"])

    df["Jour"] = df["Date"].dt.day
    df["Mois"] = df["Date"].dt.month_name()
    df["Annee"] = df["Date"].dt.year
    df["Heure"] = df["Date"].dt.hour

    return df


df = charger_donnees()

# ==========================================================
# TITRE
# ==========================================================

st.title("📊 Analyse exploratoire des données")

st.write(
    "Cette page présente une analyse descriptive du jeu de données des transactions bancaires."
)

st.markdown("---")

# ==========================================================
# APERÇU DES DONNÉES
# ==========================================================

st.subheader("📋 Aperçu du jeu de données")

st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")

# ==========================================================
# INFORMATIONS GÉNÉRALES
# ==========================================================

st.subheader("📈 Informations générales")

c1, c2, c3 = st.columns(3)

c1.metric("Nombre de lignes", df.shape[0])
c2.metric("Nombre de colonnes", df.shape[1])
c3.metric("Valeurs manquantes", int(df.isnull().sum().sum()))

st.markdown("---")

# ==========================================================
# TYPES DE DONNÉES
# ==========================================================

st.subheader("🗂 Types des variables")

types = pd.DataFrame({
    "Variable": df.columns,
    "Type": df.dtypes.astype(str)
})

st.dataframe(types, use_container_width=True)

st.markdown("---")

# ==========================================================
# STATISTIQUES DESCRIPTIVES
# ==========================================================

st.subheader("📊 Statistiques descriptives")

st.dataframe(df.describe(include="all"), use_container_width=True)

st.markdown("---")

# ==========================================================
# RÉPARTITION DES CLASSES
# ==========================================================

st.subheader("🥧 Répartition des classes")

fig = px.pie(
    df,
    names="Target",
    hole=0.45,
    color="Target",
    color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# DISTRIBUTION DES MONTANTS
# ==========================================================

st.subheader("💰 Distribution des montants")

fig = px.histogram(
    df,
    x="Montant",
    nbins=30,
    color="Target",
    title="Montant des transactions"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# TYPE DE TRANSACTION
# ==========================================================

st.subheader("💳 Type de transaction")

type_df = (
    df["Type de transaction"]
    .value_counts()
    .reset_index()
)

type_df.columns = ["Type de transaction", "Nombre"]

fig = px.bar(
    type_df,
    x="Type de transaction",
    y="Nombre",
    color="Nombre"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# LOCALISATION
# ==========================================================

st.subheader("📍 Transactions par localisation")

loc = (
    df["Localisation"]
    .value_counts()
    .reset_index()
)

loc.columns = ["Localisation", "Nombre"]

fig = px.bar(
    loc,
    x="Localisation",
    y="Nombre",
    color="Nombre"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# EVOLUTION MENSUELLE
# ==========================================================

st.subheader("📅 Évolution mensuelle")

ordre = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

mois = (
    df.groupby("Mois")
      .size()
      .reset_index(name="Transactions")
)

mois["Mois"] = pd.Categorical(
    mois["Mois"],
    categories=ordre,
    ordered=True
)

mois = mois.sort_values("Mois")

fig = px.line(
    mois,
    x="Mois",
    y="Transactions",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# BOÎTE À MOUSTACHES
# ==========================================================

st.subheader("📦 Analyse des montants")

fig = px.box(
    df,
    x="Target",
    y="Montant",
    color="Target"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# CORRÉLATION
# ==========================================================

st.subheader("🔍 Corrélation des variables numériques")

corr = df.select_dtypes(include="number").corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.success("✅ Analyse exploratoire terminée.")