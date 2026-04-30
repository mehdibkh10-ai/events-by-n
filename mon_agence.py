import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuration
st.set_page_config(page_title="Events by N - Gestion Client", layout="wide")

# 2. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Design Noir et Or
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #D4AF37; }
    .stButton>button { background-color: #D4AF37 !important; color: #000 !important; font-weight: bold !important; width: 100%; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37 !important; }
    input { border-color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Chargement des données
columns = ["Nom", "Prénom", "Âge", "Email", "Numéro", "Type", "Lieu", "Date_JMA", "Debut", "Fin"]
try:
    df = conn.read(ttl=0).astype(str)
except:
    df = pd.DataFrame(columns=columns)

# 5. Interface
st.title("✨ Events by N : Fiche Client")

with st.form("fiche_client", clear_on_submit=True):
    st.subheader("👤 Informations Personnelles")
    c1, c2, c3 = st.columns([2, 2, 1])
    nom = c1.text_input("Nom")
    prenom = c2.text_input("Prénom")
    age = c3.number_input("Âge", min_value=0, max_value=120)
    
    c4, c5 = st.columns(2)
    email = c4.text_input("Email")
    numero = c5.text_input("Numéro de téléphone")

    st.divider()
    
    st.subheader("📅 Détails de l'Événement")
    c6, c7 = st.columns(2)
    type_ev = c6.selectbox("Type d'événement", ["Mariage", "Fiançailles", "Anniversaire", "Circoncision", "Séminaire", "Autre"])
    lieu = c7.text_input("Lieu de l'événement")
    
    c8, c9, c10 = st.columns(3)
    date_ev = c8.date_input("Date (J/M/A)")
    h_debut = c9.time_input("Heure de Début")
    h_fin = c10.time_input("Heure de Fin")

    submit = st.form_submit_button("ENREGISTRER LA FICHE CLIENT")

    if submit:
        if nom and prenom and numero:
            # Formatage de la date en JJ/MM/AAAA
            date_formatee = date_ev.strftime("%d/%m/%Y")
            
            nouvelle_entree = pd.DataFrame([{
                "Nom": nom,
                "Prénom": prenom,
                "Âge": str(age),
                "Email": email,
                "Numéro": str(numero),
                "Type": type_ev,
                "Lieu": lieu,
                "Date_JMA": date_formatee,
                "Debut": str(h_debut),
                "Fin": str(h_fin)
            }])
            
            # Mise à jour
            updated_df = pd.concat([df, nouvelle_entree], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success(f"✅ Fiche de {prenom} {nom} enregistrée !")
            st.balloons()
        else:
            st.error("⚠️ Merci de remplir au moins le Nom, le Prénom et le Numéro.")

st.divider()
st.subheader("📊 Liste des Dossiers")
st.dataframe(df, use_container_width=True)
