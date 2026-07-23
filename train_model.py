# ============================================================
# PROJET : Détection de fraude bancaire
# Fichier : train_model.py
# ============================================================

# Importation des bibliothèques

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import joblib

import warnings
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
warnings.filterwarnings("ignore")

# ============================================================
# Chargement des données
# ============================================================

chemin = "data/Bank_transaction_scenario1.csv"

df = pd.read_csv(chemin, sep=";")

# ============================================================
# Informations générales
# ============================================================

print("=" * 60)
print("APERÇU DU JEU DE DONNÉES")
print("=" * 60)

print(df.head())

print("\n")

print("=" * 60)
print("DIMENSIONS")
print("=" * 60)

print(df.shape)

print("\n")

print("=" * 60)
print("NOMS DES COLONNES")
print("=" * 60)

print(df.columns)

print("\n")

print("=" * 60)
print("TYPES DES DONNÉES")
print("=" * 60)

print(df.dtypes)

# ============================================================
# VALEURS MANQUANTES
# ============================================================

print("\n" + "=" * 60)
print("VALEURS MANQUANTES")
print("=" * 60)

print(df.isnull().sum())

# ============================================================
# DOUBLONS
# ============================================================

print("\n" + "=" * 60)
print("NOMBRE DE DOUBLONS")
print("=" * 60)

print(df.duplicated().sum())

# ============================================================
# STATISTIQUES DES VARIABLES NUMÉRIQUES
# ============================================================

print("\n" + "=" * 60)
print("STATISTIQUES")
print("=" * 60)

print(df.describe())

# ============================================================
# RÉPARTITION DE LA VARIABLE TARGET
# ============================================================

print("\n" + "=" * 60)
print("RÉPARTITION DE TARGET")
print("=" * 60)

print(df["Target"].value_counts())

# ============================================================
# GRAPHIQUE TARGET
# ============================================================

plt.figure(figsize=(6,4))

df["Target"].value_counts().plot(kind="bar")

plt.title("Répartition des transactions")

plt.xlabel("Classe")

plt.ylabel("Nombre")

plt.tight_layout()
plt.savefig("assets/repartition_target.png")

plt.close()

# ============================================================
# CONVERSION DE LA DATE
# ============================================================

print("\nConversion de la colonne Date...")

df["Date"] = pd.to_datetime(df["Date"])

print(df["Date"].head())

# ============================================================
# EXTRACTION DES INFORMATIONS DE DATE
# ============================================================

df["Jour"] = df["Date"].dt.day
df["Mois"] = df["Date"].dt.month
df["Annee"] = df["Date"].dt.year
df["JourSemaine"] = df["Date"].dt.dayofweek

print("\nNouvelles colonnes créées :")

print(df[["Date", "Jour", "Mois", "Annee", "JourSemaine"]].head())

# ============================================================
# SUPPRESSION DES COLONNES INUTILES
# ============================================================

colonnes_supprimer = [
    "Identifiant operation",
    "Date",
    "ID Clients",
    "Numero de compte"
]


df.drop(columns=colonnes_supprimer, inplace=True)

print("\nColonnes restantes :")

print(df.columns)

# ============================================================
# ENCODAGE DES VARIABLES CATEGORIELLES
# ============================================================

print("\n" + "=" * 60)
print("ENCODAGE DES VARIABLES")
print("=" * 60)

encoders = {}

colonnes_categorielles = [
    "Type de transaction",
    "Status operation",
    "Localisation",
    "Target"
]

for col in colonnes_categorielles:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

joblib.dump(encoders, "model/encoder.pkl")

print("Encodage terminé.")
print(df.head())
# ============================================================
# VARIABLES EXPLICATIVES ET CIBLE
# ============================================================

X = df.drop("Target", axis=1)
print("\nColonnes utilisées pour entraîner le modèle :")
print(X.columns.tolist())

y = df["Target"]

print("\nDimensions de X :", X.shape)
print("Dimensions de y :", y.shape)
# ============================================================
# TRAIN / TEST
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain :", X_train.shape)
print("Test :", X_test.shape)
# ============================================================
# STANDARDISATION
# ============================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

joblib.dump(scaler, "model/scaler.pkl")

print("\nStandardisation effectuée.")
from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import SVC

from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score
# ============================================================
# MODELES
# ============================================================

modeles = {

    "Régression Logistique":
        LogisticRegression(max_iter=1000),

    "Arbre de Décision":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(random_state=42),

    "KNN":
        KNeighborsClassifier(),

    "SVM":
        SVC(),

    "Naive Bayes":
        GaussianNB()

}
# ============================================================
# ENTRAINEMENT
# ============================================================

print("\n" + "=" * 60)
print("RESULTATS")
print("=" * 60)

meilleur_modele = None
meilleur_score = 0

for nom, modele in modeles.items():

    modele.fit(X_train, y_train)

    prediction = modele.predict(X_test)

    score = accuracy_score(y_test, prediction)

    print(f"{nom:25s} : {score:.4f}")

    if score > meilleur_score:
        meilleur_score = score
        meilleur_modele = modele
        meilleures_predictions = prediction

print("\nMeilleur modèle :", type(meilleur_modele).__name__)
print("Accuracy :", meilleur_score)

print("\nRapport de classification")
print(classification_report(y_test, meilleures_predictions))

print("\nMatrice de confusion")
print(confusion_matrix(y_test, meilleures_predictions))

joblib.dump(meilleur_modele, "model/fraud_model.pkl")

print("\nModèle sauvegardé.")

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix