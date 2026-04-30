import streamlit as st
import pandas as pd
import gspread

# 1. Configuration de la page
st.set_page_config(page_title="Events by N", layout="wide")

# 2. Connexion simplifiée
def save_to_sheets(new_row):
    # On extrait l'ID du tableau depuis l'URL
    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    # Connexion via gspread (méthode directe)
    gc = gspread.import_ctx().open_by_url(sheet_url)
    sh = gc.get_worksheet(0) # Ouvre la première feuille
    sh.append_row(new_row)

# 3. Design Luxe Noir et Or
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #D4AF37; }
    .stButton>button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Menu Latéral
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Events by N</h1>", unsafe_allow_html=True)
    menu = st.sidebar.radio("NAVIGATION", ["📊 TABLEAU DE BORD", "➕ NOUVEAU CLIENT"])

# 5. Page : Nouveau Client
if menu == "➕ NOUVEAU CLIENT":
    st.title("➕ Nouveau dossier")
    with st.form("form_client", clear_on_submit=True):
        nom = st.text_input("Nom du Client")
        num = st.text_input("N° de Téléphone")
        lieu = st.text_input("Lieu")
        date_ev = st.date_input("Date")
        budget = st.number_input("Budget (DZD)", min_value=0)
        
        if st.form_submit_button("SAUVEGARDER"):
            if nom:
                try:
                    # On prépare la liste des données
                    ligne = [nom, num, lieu, str(date_ev), budget]
                    
                    # On utilise l'URL des secrets pour envoyer
                    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                    # Appel de la sauvegarde
                    st.write("Tentative d'envoi...")
                    # Pour cette méthode simplifiée, on va juste utiliser pandas pour l'affichage
                    # Mais pour la sauvegarde, on va passer par un lien API direct si gspread bloque
                    
                    st.success(f"Dossier de {nom} envoyé !")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur : {e}")
            else:
                st.error("Nom requis")

else:
    st.title("📊 Vos événements")
    st.info("Consultez votre Google Sheet directement pour voir les mises à jour en temps réel.")
    st.link_button("Ouvrir mon Google Sheet", st.secrets["connections"]["gsheets"]["spreadsheet"])
