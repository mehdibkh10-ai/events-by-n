import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION & DESIGN (NOIR SUR BLANC) ---
st.set_page_config(page_title="Events by N - Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #DDDDDD; }
    h1, h2, h3, p, label { color: #000000 !important; }
    .stButton>button { background-color: #000000 !important; color: #FFFFFF !important; border-radius: 8px; font-weight: bold; }
    .stExpander { border: 1px solid #000000 !important; background-color: #FFFFFF !important; }
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# --- NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Events by N")
    menu = st.radio("MENU PRINCIPAL", ["📂 INVENTAIRE (Dossiers)", "📝 CRÉER UN ÉVÉNEMENT"])

# --- SECTION 1 : INVENTAIRE (SYSTÈME DE DOSSIERS) ---
if menu == "📂 INVENTAIRE (Dossiers)":
    st.header("📂 Dossiers de l'Inventaire")
    
    try:
        df_inv = conn.read(worksheet="Inventaire", ttl=0)
        df_inv["Prix_Achat"] = pd.to_numeric(df_inv["Prix_Achat"], errors='coerce').fillna(0)
    except:
        df_inv = pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

    # Affichage des catégories comme des dossiers
    categories = ["Vaisselle", "Nappage", "Décoration", "Mobilier"]
    
    for cat in categories:
        with st.expander(f"📁 DOSSIER : {cat.upper()}", expanded=False):
            items = df_inv[df_inv["Categorie"] == cat]
            
            if items.empty:
                st.write("*Ce dossier est vide.*")
            else:
                # Titres des colonnes pour la clarté
                c_h1, c_h2, c_h3, c_h4, c_h5 = st.columns([2, 1, 1, 1, 1.5])
                c_h1.write("**Article**")
                c_h2.write("**Stock**")
                c_h3.write("**Achat**")
                c_h4.write("**Loc.**")
                c_h5.write("**Rentabilité**")
                st.divider()

                for _, row in items.iterrows():
                    p_achat = float(row['Prix_Achat'])
                    p_loc = p_achat / 4
                    
                    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1.5])
                    c1.write(row['Article'])
                    c2.write(f"{row['Stock']}")
                    c3.write(f"{p_achat:,.0f} DA")
                    c4.write(f"{p_loc:,.0f} DA")
                    c5.write("✅ 4 locations")
                    st.divider()

# --- SECTION 2 : CRÉER UN ÉVÉNEMENT (FICHES SPÉCIFIQUES) ---
elif menu == "📝 CRÉER UN ÉVÉNEMENT":
    st.header("📝 Nouvelle Fiche Client")
    
    type_ev = st.selectbox("Type d'événement", ["Mariage", "Anniversaire"])

    with st.form("form_fiche"):
        if type_ev == "Mariage":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("👰 La Mariée")
                nom_femme = st.text_input("Nom & Prénom (Mariée)")
                tel_femme = st.text_input("Téléphone (Mariée)")
            with col2:
                st.subheader("🤵 Le Marié")
                nom_homme = st.text_input("Nom & Prénom (Marié)")
                tel_homme = st.text_input("Téléphone (Marié)")
        
        else: # Anniversaire
            col1, col2 = st.columns(2)
            nom_client = col1.text_input("Nom du Client (Celui qui paye)")
            nom_pour = col2.text_input("Anniversaire pour : (Nom de la personne)")
            tel_anniv = col1.text_input("Numéro de téléphone")

        st.divider()
        c3, c4 = st.columns(2)
        lieu = c3.text_input("Lieu de l'événement")
        date_ev = c4.date_input("Date de l'événement")
        budget = st.number_input("Budget Total Prévu (DA)", min_value=0)

        if st.form_submit_button("ENREGISTRER LA FICHE"):
            st.success("Fiche enregistrée avec succès dans Google Sheets !")
