import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Config & Style Luxe
st.set_page_config(page_title="Events by N - Gestion Totale", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #D4AF37; }
    .stButton>button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stTab { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Menu Latéral
with st.sidebar:
    st.title("⚜️ Events by N")
    menu = st.radio("NAVIGATION", ["✨ NOUVEL ÉVÉNEMENT", "📦 MON INVENTAIRE", "📊 DOSSIERS EN COURS"])

# --- PAGE 1 : CRÉATION ÉVÉNEMENT ---
if menu == "✨ NOUVEL ÉVÉNEMENT":
    st.header("🪄 Créer un nouvel événement")
    
    type_ev = st.selectbox("Quel type d'événement ?", ["Mariage", "Anniversaire", "Fiançailles", "Séminaire"])
    
    with st.form("form_event"):
        col1, col2 = st.columns(2)
        
        if type_ev == "Mariage":
            st.subheader("👰 Fiche de la Mariée")
            nom_m = col1.text_input("Nom de la Mariée")
            tel_m = col1.text_input("Téléphone Mariée")
            
            st.subheader("🤵 Fiche du Marié")
            nom_h = col2.text_input("Nom du Marié")
            tel_h = col2.text_input("Téléphone Marié")
            client_final = f"{nom_m} & {nom_h}"
        
        elif type_ev == "Anniversaire":
            st.subheader("🎂 Fiche de l'Anniversaire")
            nom_c = col1.text_input("Nom de la personne")
            tel_c = col1.text_input("Téléphone")
            client_final = nom_c

        st.divider()
        lieu = st.text_input("Lieu de l'événement")
        date_ev = st.date_input("Date prévue")
        budget = st.number_input("Budget (DZD)", min_value=0)

        if st.form_submit_button("VALIDER L'ÉVÉNEMENT"):
            st.success(f"Événement '{type_ev}' de {client_final} enregistré !")
            # Logique de sauvegarde ici vers l'onglet Clients

# --- PAGE 2 : INVENTAIRE ---
elif menu == "📦 MON INVENTAIRE":
    st.header("🍽️ Gestion du Matériel")
    
    tab1, tab2 = st.tabs(["📋 Liste du Stock", "➕ Ajouter du Matériel"])
    
    with tab2:
        with st.form("add_stock"):
            c1, c2, c3 = st.columns(3)
            item = c1.text_input("Nom de l'article (ex: Verre Cristal)")
            cat = c2.selectbox("Catégorie", ["Vaisselle", "Nappage", "Décoration", "Mobilier"])
            quantite = c3.number_input("Quantité en stock", min_value=0)
            
            if st.form_submit_button("AJOUTER AU STOCK"):
                st.info(f"{quantite} {item} ajoutés à l'inventaire.")

    with tab1:
        # Ici on affichera le tableau lu depuis l'onglet 'Inventaire'
        st.write("### État actuel de votre matériel")
        # Exemple de ce qu'on verrait :
        data_inv = {
            "Article": ["Assiette Dorée", "Nappe Satin", "Verre à pied"],
            "Catégorie": ["Vaisselle", "Nappage", "Vaisselle"],
            "Stock": [150, 40, 200]
        }
        st.table(data_inv)

# --- PAGE 3 : DOSSIERS ---
else:
    st.header("📊 Dossiers & Suivi")
    st.info("Cette section affiche tous vos contrats en cours extraits de Google Sheets.")
