import streamlit as st
import pandas as pd
import joblib
import os

# ==========================
# Configuration de la page
# ==========================
st.set_page_config(
    page_title="Prédiction",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Prédiction d'une transaction bancaire")
st.write("Complétez les informations ci-dessous puis cliquez sur **Prédire**.")

# ==========================
# Chargement des fichiers
# ==========================
try:
    model = joblib.load(os.path.join("model", "fraud_model.pkl"))
    scaler = joblib.load(os.path.join("model", "scaler.pkl"))
    encoders = joblib.load(os.path.join("model", "encoder.pkl"))
    st.success("✅ Modèle chargé avec succès.")
except Exception as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

# ==========================
# Formulaire
# ==========================
st.subheader("📋 Informations de la transaction")

col1, col2 = st.columns(2)

with col1:
    montant = st.number_input(
        "Montant (FCFA)",
        min_value=0.0,
        value=1000.0,
        step=1000.0
    )

    type_transaction = st.selectbox(
        "Type de transaction",
        encoders["Type de transaction"].classes_
    )

    status = st.selectbox(
        "Statut de l'opération",
        encoders["Status operation"].classes_
    )

with col2:
    localisation = st.selectbox(
        "Localisation",
        encoders["Localisation"].classes_
    )

    jour = st.slider("Jour", 1, 31, 15)

    mois = st.slider("Mois", 1, 12, 7)

    annee = st.number_input(
        "Année",
        min_value=2020,
        max_value=2035,
        value=2025
    )

    jour_semaine = st.selectbox(
        "Jour de la semaine",
        [0,1,2,3,4,5,6],
        format_func=lambda x: [
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche"
        ][x]
    )

# ==========================
# Prédiction
# ==========================
if st.button("🔍 Prédire", use_container_width=True):

    data = pd.DataFrame({

        "Type de transaction":[
            encoders["Type de transaction"].transform([type_transaction])[0]
        ],

        "Status operation":[
            encoders["Status operation"].transform([status])[0]
        ],

        "Localisation":[
            encoders["Localisation"].transform([localisation])[0]
        ],

        "Montant":[montant],

        "Jour":[jour],

        "Mois":[mois],

        "Annee":[annee],

        "JourSemaine":[jour_semaine]

    })

    # Respect de l'ordre des variables utilisé pendant l'entraînement
    data = data[
        [
            "Type de transaction",
            "Status operation",
            "Localisation",
            "Montant",
            "Jour",
            "Mois",
            "Annee",
            "JourSemaine"
        ]
    ]

    st.subheader("📋 Résumé de la transaction")
    st.dataframe(data, use_container_width=True)

    data_scaled = scaler.transform(data)

    prediction = model.predict(data_scaled)

    proba = model.predict_proba(data_scaled)[0]

    resultat = encoders["Target"].inverse_transform(prediction)[0]

    st.subheader("📊 Probabilités")

    classes = encoders["Target"].classes_

    for classe, p in zip(classes, proba):
        st.progress(float(p))
        st.write(f"**{classe} : {p*100:.2f}%**")

    st.divider()

    st.subheader("🎯 Résultat de la prédiction")

    if resultat == "Fraude":
        st.error("🚨 **Transaction Frauduleuse**")

    elif resultat == "Suspect":
        st.warning("⚠️ **Transaction Suspecte**")

    else:
        st.success("✅ **Transaction Normale**")