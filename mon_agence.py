import streamlit as st
import streamlit as st
import json
import os

# 1. Configuration
st.set_page_config(page_title="Events by N - Sauvegarde Auto", layout="wide")

# --- SYSTÈME DE SAUVEGARDE SUR DISQUE ---
FICHIER_DATA = "base_donnees_events.json"

def charger_donnees():
    if os.path.exists(FICHIER_DATA):
        with open(FICHIER_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_donnees(liste_clients):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(liste_clients, f, indent=4, ensure_ascii=False)

# Initialisation
if 'clients' not in st.session_state:
    st.session_state.clients = charger_donnees()
if 'client_idx' not in st.session_state:
    st.session_state.client_idx = None

# --- DESIGN LUXE DARK ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #D4AF37; }
    .metric-card {
        background-color: #1E1E1E; padding: 20px; border-radius: 15px;
        border: 1px solid #D4AF37; text-align: center;
    }
    .stButton>button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold !important; border-radius: 10px !important; }
    input, textarea, select { background-color: #2D2D2D !important; color: white !important; }
    label { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("<h1 style='color: #D4AF37; text-align: center;'>Events by N</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENU", ["📊 TABLEAU DE BORD", "➕ NOUVEAU CLIENT"])
    st.write("---")
    st.subheader("👥 MES DOSSIERS")
    
    # Affichage des clients sauvegardés
    for i, c in enumerate(st.session_state.clients):
        if st.button(f"👤 {c['nom']}", key=f"user_{i}"):
            st.session_state.client_idx = i

# --- PAGES ---

if menu == "➕ NOUVEAU CLIENT":
    st.title("➕ Créer une fiche")
    with st.form("form_permanent"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom & Prénom")
            num = st.text_input("Téléphone")
            adresse = st.text_area("Adresse")
        with c2:
            lieu = st.text_input("Lieu")
            date = st.date_input("Date")
            h_debut = st.time_input("Début")
            h_fin = st.time_input("Fin")
            budget = st.number_input("Budget (DZD)", min_value=0)
        
        if st.form_submit_button("SAUVEGARDER DÉFINITIVEMENT"):
            if nom:
                nouvelle_fiche = {
                    "nom": nom, "num": num, "adresse": adresse,
                    "lieu": lieu, "date": str(date), "debut": str(h_debut), "fin": str(h_fin),
                    "budget": budget
                }
                # Ajouter à la liste ET sauvegarder dans le fichier
                st.session_state.clients.append(nouvelle_fiche)
                sauvegarder_donnees(st.session_state.clients)
                st.success(f"Dossier de {nom} enregistré sur le disque !")
                st.rerun()

elif menu == "📊 TABLEAU DE BORD":
    if st.session_state.client_idx is not None:
        c = st.session_state.clients[st.session_state.client_idx]
        st.markdown(f"<h1 style='color: #D4AF37;'>Dossier : {c['nom']}</h1>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        col_a.info(f"📍 Lieu : {c['lieu']} | 📅 Date : {c['date']}")
        col_b.info(f"⏰ Horaires : {c['debut']} - {c['fin']}")
        
        st.write("##")
        m1, m2 = st.columns(2)
        m1.markdown(f"<div class='metric-card'><h3>BUDGET ALLOUÉ</h3><h2>{c['budget']:,} DZD</h2></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='metric-card'><h3>CONTACT</h3><h2>{c['num']}</h2></div>", unsafe_allow_html=True)
    else:
        st.info("Sélectionnez un client à gauche pour voir ses informations.")
