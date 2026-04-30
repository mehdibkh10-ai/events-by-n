import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Events by N", layout="wide")

# 2. Connexion à Google Sheets
# On récupère l'URL directement depuis les secrets pour éviter les erreurs
sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
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

# 4. Chargement des données
try:
    # On lit le tableau actuel
    df = conn.read(spreadsheet=sheet_url, ttl=0).astype(str)
except Exception as e:
    # Si le tableau est vide, on crée les colonnes par défaut
    df = pd.DataFrame(columns=["nom", "num", "adresse", "lieu", "date", "budget"])

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
        
        submit = st.form_submit_button("SAUVEGARDER DANS LE CLOUD")
        
        if submit:
            if nom:
                # Préparation de la nouvelle ligne
                nouveau_client = pd.DataFrame([{
                    "nom": nom, 
                    "num": str(num), 
                    "adresse": adresse,
                    "lieu": lieu, 
                    "date": str(date_ev), 
                    "budget": str(budget)
                }])
                
                # Fusion avec les anciens clients
                updated_df = pd.concat([df, nouveau_client], ignore_index=True)
                
                # SAUVEGARDE CRITIQUE
                try:
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success(f"✅ Dossier de {nom} enregistré avec succès !")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur de connexion : Vérifie que ton Google Sheet est bien en mode 'Éditeur' pour tout le monde.")
            else:
                st.error("⚠️ Le nom du client est obligatoire.")

# 7. Page : Tableau de Bord
else:
    st.title("📊 Liste de tes événements")
    # On ré-affiche le tableau mis à jour
    st.dataframe(df, use_container_width=True)
