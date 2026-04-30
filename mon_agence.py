import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Events by N", layout="wide")

# 2. Connexion à Google Sheets (utilise les Secrets que tu as configurés)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Design Luxe Noir et Or
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #D4AF37; }
    .stButton>button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stDataFrame { background-color: #1E1E1E; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 4. Chargement des données (avec sécurité)
try:
    df = conn.read(ttl=0).astype(str)
except:
    df = pd.DataFrame(columns=["nom", "num", "adresse", "lieu", "date", "debut", "fin", "budget"])

# 5. Menu Latéral
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Events by N</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.sidebar.radio("NAVIGATION", ["📊 TABLEAU DE BORD", "➕ NOUVEAU CLIENT"])

# 6. Page : Nouveau Client
if menu == "➕ NOUVEAU CLIENT":
    st.title("➕ Enregistrer un nouveau dossier")
    with st.form("form_client", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom du Client")
            num = st.text_input("N° de Téléphone")
            adresse = st.text_area("Adresse du client")
        with col2:
            lieu = st.text_input("Lieu de l'événement")
            date_ev = st.date_input("Date de l'événement")
            budget = st.number_input("Budget Total (DZD)", min_value=0)
        
        if st.form_submit_button("SAUVEGARDER DANS LE CLOUD"):
            if nom:
                # Création de la nouvelle ligne
                nouveau_client = pd.DataFrame([{
                    "nom": nom, "num": num, "adresse": adresse,
                    "lieu": lieu, "date": str(date_ev), "budget": str(budget)
                }])
                # Mise à jour du Google Sheets
                updated_df = pd.concat([df, nouveau_client], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"✅ Le dossier de {nom} a été sauvegardé sur ton Google Sheets !")
            else:
                st.error("⚠️ Merci d'entrer au moins le nom du client.")

# 7. Page : Tableau de Bord
else:
    st.title("📊 Liste de tes événements")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun client enregistré pour le moment.")
