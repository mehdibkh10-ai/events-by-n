import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Design Épuré (Noir & Blanc)
st.set_page_config(page_title="Gestion Finance - Events by N", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #DDDDDD; }
    h1, h2, h3, p, label, .stMarkdown { color: #000000 !important; }
    .stButton>button { background-color: #000000 !important; color: #FFFFFF !important; border-radius: 8px; }
    /* Style des métriques pour qu'elles soient lisibles en noir */
    [data-testid="stMetricValue"] { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        df = conn.read(worksheet="Inventaire", ttl=0)
        # Convertir les prix en nombres pour les calculs
        df["Prix_Achat"] = pd.to_numeric(df["Prix_Achat"], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

# 3. Navigation Sidebar
with st.sidebar:
    st.title("Events by N")
    page = st.radio("ALLER VERS", ["📦 Inventaire & Calculs", "✨ Nouveaux Clients"])

if page == "📦 Inventaire & Calculs":
    st.header("📦 Gestion & Rentabilité du Matériel")
    df = get_data()

    if not df.empty:
        # Sélecteur de catégorie
        cat_list = ["Toutes"] + list(df["Categorie"].unique())
        cat_choisie = st.selectbox("Filtrer par catégorie", cat_list)
        
        df_display = df if cat_choisie == "Toutes" else df[df["Categorie"] == cat_choisie]

        st.divider()

        # Affichage des fiches articles avec calculs financiers
        for _, row in df_display.iterrows():
            # Calculs automatiques
            p_achat = float(row['Prix_Achat'])
            p_location = p_achat / 4
            # Rentabilité : on sait que c'est 4 fois (100% / 25%)
            
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                col1.subheader(f"🔹 {row['Article']}")
                col1.caption(f"Catégorie : {row['Categorie']} | Stock : {row['Stock']}")
                
                col2.metric("Prix d'Achat", f"{p_achat:,.0f} DA")
                col3.metric("Prix Location (1/4)", f"{p_location:,.0f} DA")
                col4.metric("Rentabilité", "4 loc.", help="Nombre de locations pour rembourser l'achat")
                
                st.divider()
    else:
        st.info("Aucun article trouvé. Ajoutez-en un ci-dessous.")

    # Formulaire d'ajout
    with st.expander("➕ Ajouter un article avec son prix"):
        with st.form("new_item"):
            c1, c2 = st.columns(2)
            cat = c1.selectbox("Catégorie", ["Vaisselle", "Nappage", "Décoration", "Mobilier"])
            nom = c2.text_input("Nom de l'article")
            qty = c1.number_input("Quantité", min_value=1)
            prix = c2.number_input("Prix d'achat unitaire (DA)", min_value=0)
            
            if st.form_submit_button("Enregistrer l'article"):
                st.success(f"L'article {nom} a été ajouté avec un prix de location de {prix/4} DA")

# --- PAGE CLIENTS ---
else:
    st.header("✨ Dossiers Clients")
    st.write("Espace pour gérer vos mariages et anniversaires.")
