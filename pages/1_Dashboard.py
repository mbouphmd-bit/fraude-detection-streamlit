import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# CONFIGURATION DE LA PAGE
# ==========================================================
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LECTURE DES DONNÉES
# ==========================================================
@st.cache_data
def charger_donnees():

    df = pd.read_csv(
        "data/Bank_transaction_scenario1.csv",
        sep=";"
    )

    # Conversion de la date
    df["Date"] = pd.to_datetime(df["Date"])

    # Création de nouvelles colonnes
    df["Jour"] = df["Date"].dt.day
    df["Mois"] = df["Date"].dt.month_name()
    df["Annee"] = df["Date"].dt.year
    df["Heure"] = df["Date"].dt.hour
    df["JourSemaine"] = df["Date"].dt.day_name()

    return df


# Chargement des données
df = charger_donnees()

# ==========================================================
# TITRE
# ==========================================================
st.title("🏦 Dashboard de Détection de Fraude Bancaire")

st.markdown(
    """
    Ce tableau de bord permet d'analyser les transactions bancaires,
    d'identifier les opérations suspectes et de visualiser les indicateurs
    clés liés à la fraude.
    """
)

st.markdown("---")

# ==========================================================
# BARRE LATÉRALE
# ==========================================================
st.sidebar.header("🎛️ Filtres")

type_transaction = st.sidebar.multiselect(
    "Type de transaction",
    options=sorted(df["Type de transaction"].unique()),
    default=sorted(df["Type de transaction"].unique())
)

localisation = st.sidebar.multiselect(
    "Localisation",
    options=sorted(df["Localisation"].unique()),
    default=sorted(df["Localisation"].unique())
)

classe = st.sidebar.multiselect(
    "Classe",
    options=sorted(df["Target"].unique()),
    default=sorted(df["Target"].unique())
)

# ==========================================================
# APPLICATION DES FILTRES
# ==========================================================
df = df[
    (df["Type de transaction"].isin(type_transaction))
    &
    (df["Localisation"].isin(localisation))
    &
    (df["Target"].isin(classe))
]

# ==========================================================
# CALCUL DES KPI
# ==========================================================
total_transactions = len(df)

montant_total = df["Montant"].sum()

montant_moyen = df["Montant"].mean()

nombre_normales = (df["Target"] == "Normal").sum()

nombre_suspectes = (df["Target"] == "Suspect").sum()

nombre_fraudes = (df["Target"] == "Fraude").sum()

# ==========================================================
# AFFICHAGE DES KPI
# ==========================================================
st.subheader("📈 Indicateurs clés")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Transactions",
        value=f"{total_transactions:,}"
    )

with col2:
    st.metric(
        label="Montant total",
        value=f"{montant_total:,.0f} FCFA"
    )

with col3:
    st.metric(
        label="Montant moyen",
        value=f"{montant_moyen:,.0f} FCFA"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="Normales",
        value=nombre_normales
    )

with col5:
    st.metric(
        label="Suspectes",
        value=nombre_suspectes
    )

with col6:
    st.metric(
        label="Fraudes",
        value=nombre_fraudes
    )

st.markdown("---")
# ==========================================================
# GRAPHIQUES
# ==========================================================

st.subheader("📊 Analyse des transactions")

col1, col2 = st.columns(2)

# -----------------------------
# Diagramme circulaire
# -----------------------------
with col1:

    fig = px.pie(
        df,
        names="Target",
        title="Répartition des classes",
        hole=0.45,
        color="Target",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Histogramme des montants
# -----------------------------
with col2:

    fig = px.histogram(
        df,
        x="Montant",
        color="Target",
        nbins=30,
        title="Distribution des montants",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# LOCALISATION ET TYPE DE TRANSACTION
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)

# -----------------------------
# Transactions par localisation
# -----------------------------
with col1:

    localisation_df = (
        df.groupby("Localisation")
          .size()
          .reset_index(name="Nombre")
          .sort_values("Nombre", ascending=False)
    )

    fig = px.bar(
        localisation_df,
        x="Localisation",
        y="Nombre",
        color="Nombre",
        title="Transactions par localisation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Transactions par type
# -----------------------------
with col2:

    type_df = (
        df.groupby("Type de transaction")
          .size()
          .reset_index(name="Nombre")
          .sort_values("Nombre", ascending=False)
    )

    fig = px.bar(
        type_df,
        x="Type de transaction",
        y="Nombre",
        color="Nombre",
        title="Types de transaction"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# EVOLUTION MENSUELLE
# ==========================================================

st.markdown("---")

ordre_mois = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

mois_df = (
    df.groupby("Mois")
      .size()
      .reset_index(name="Transactions")
)

mois_df["Mois"] = pd.Categorical(
    mois_df["Mois"],
    categories=ordre_mois,
    ordered=True
)

mois_df = mois_df.sort_values("Mois")

fig = px.line(
    mois_df,
    x="Mois",
    y="Transactions",
    markers=True,
    title="Évolution mensuelle des transactions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# TRANSACTIONS PAR HEURE
# ==========================================================

st.markdown("---")

heure_df = (
    df.groupby("Heure")
      .size()
      .reset_index(name="Transactions")
      .sort_values("Heure")
)

fig = px.bar(
    heure_df,
    x="Heure",
    y="Transactions",
    color="Transactions",
    title="Transactions par heure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# BOITE A MOUSTACHES
# ==========================================================

st.markdown("---")

fig = px.box(
    df,
    x="Target",
    y="Montant",
    color="Target",
    title="Montants des transactions selon la classe"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# ==========================================================
# TABLEAU DES TRANSACTIONS
# ==========================================================

st.subheader("📋 Dernières transactions")

st.dataframe(
    df.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# STATISTIQUES DESCRIPTIVES
# ==========================================================

st.markdown("---")

st.subheader("📈 Statistiques descriptives")

stats = df["Montant"].describe()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Montant minimum",
        f"{stats['min']:,.0f} FCFA"
    )

with col2:
    st.metric(
        "Montant maximum",
        f"{stats['max']:,.0f} FCFA"
    )

with col3:
    st.metric(
        "Écart-type",
        f"{stats['std']:,.0f} FCFA"
    )

with col4:
    st.metric(
        "Médiane",
        f"{df['Montant'].median():,.0f} FCFA"
    )

# ==========================================================
# RÉPARTITION DES CLASSES
# ==========================================================

st.markdown("---")

st.subheader("📊 Répartition détaillée")

resume = (
    df.groupby("Target")
      .agg(
          Nombre=("Target", "count"),
          Montant_Total=("Montant", "sum"),
          Montant_Moyen=("Montant", "mean")
      )
      .reset_index()
)

st.dataframe(
    resume,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# EXPORT CSV
# ==========================================================

st.markdown("---")

st.subheader("📥 Export des données filtrées")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Télécharger les données (CSV)",
    data=csv,
    file_name="transactions_filtrees.csv",
    mime="text/csv"
)

# ==========================================================
# PIED DE PAGE
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:gray; font-size:14px;'>

    🏦 <b>Système Intelligent de Détection de Fraude Bancaire</b><br>

    Réalisé avec <b>Python</b>, <b>Streamlit</b> et <b>Plotly</b><br>

    Master Intelligence Artificielle – DIT

    </div>
    """,
    unsafe_allow_html=True
)
