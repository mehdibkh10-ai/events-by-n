import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION ET STYLE NOIR SUR BLANC ---
st.set_page_config(page_title="Events by N - Gestion de Stock", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #DDDDDD; }
    h1, h2, h3, p, label { color: #000000 !important; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #000000 !important; color: #FFFFFF !important; border-radius: 5px; width: 100%; }
    .stExpander { border: 1px solid #EEEEEE !important; box-shadow: none !important; }
    [data-testid="stMetricValue"] { color: #000000 !important; font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_inventory():
    try:
        df = conn.read(worksheet="Inventaire", ttl=0)
        df["Prix_Achat"] = pd.to_numeric(df["Prix_Achat"], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

# --- NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Events by N")
    menu = st.radio("NAVIGATION", ["📦 MON INVENTAIRE", "📝 NOUVELLE FICHE CLIENT"])

# --- SECTION 1 : INVENTAIRE (ORGANISATION PROFESSIONNELLE) ---
if menu == "📦 MON INVENTAIRE":
    st.header("📦 Gestion Stratégique du Stock")
    df_inv = load_inventory()

    # Catégories basées sur ton texte
    categories_pros = [
        "1. Mobilier & Structures", 
        "2. Textiles & Linge", 
        "3. Verrerie & Vaisselle", 
        "4. Papeterie & Signalétique", 
        "5. Éclairage & Ambiance",
        "6. Matériel Technique"
    ]

    for cat in categories_pros:
        with st.expander(f"📂 {cat.upper()}", expanded=False):
            # Filtrage des articles
            items = df_inv[df_inv["Categorie"] == cat]
            
            if items.empty:
                st.write("*Aucun article enregistré dans cette catégorie.*")
            else:
                # En-tête du tableau
                c_h1, c_h2, c_h3, c_h4, c_h5 = st.columns([2, 1, 1, 1, 1])
                c_h1.write("**Désignation**")
                c_h2.write("**Stock**")
                c_h3.write("**Prix Achat**")
                c_h4.write("**Location (1/4)**")
                c_h5.write("**Rentabilité**")
                st.divider()

                for _, row in items.iterrows():
                    p_achat = float(row['Prix_Achat'])
                    p_loc = p_achat / 4 # Règle du 1/4
                    
                    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
                    c1.write(f"🔹 {row['Article']}")
                    c2.write(f"{row['Stock']}")
                    c3.write(f"{p_achat:,.0f} DA")
                    c4.write(f"**{p_loc:,.0f} DA**")
                    c5.write("🎯 4 locations")
                    st.divider()

    # Formulaire d'ajout rapide
    with st.expander("➕ AJOUTER UN NOUVEL ARTICLE AU STOCK"):
        with st.form("add_stock"):
            c_a, c_b = st.columns(2)
            new_cat = c_a.selectbox("Catégorie", categories_pros)
            new_art = c_b.text_input("Nom de l'article (ex: Arches rondes)")
            new_qty = c_a.number_input("Quantité", min_value=1)
            new_prx = c_b.number_input("Prix d'achat unitaire (DA)", min_value=0)
            
            if st.form_submit_button("ENREGISTRER DANS LE STOCK"):
                st.success(f"L'article {new_art} est prêt à être loué pour {new_prx/4} DA !")

# --- SECTION 2 : FICHES CLIENTS ---
else:
    st.header("📝 Création de Dossier")
    type_ev = st.selectbox("Type d'événement", ["Mariage", "Anniversaire"])

    with st.form("fiche_client"):
        if type_ev == "Mariage":
            c1, c2 = st.columns(2)
            c1.subheader("👰 La Mariée")
            n_f = c1.text_input("Nom & Prénom")
            t_f = c1.text_input("Téléphone")
            
            c2.subheader("🤵 Le Marié")
            n_h = c2.text_input("Nom & Prénom ")
            t_h = c2.text_input("Téléphone ")
        else:
            c1, c2 = st.columns(2)
            n_c = c1.text_input("Nom du Client")
            n_p = c2.text_input("Anniversaire pour :")
            t_c = c1.text_input("Téléphone")

        st.divider()
        lieu = st.text_input("Lieu de l'événement")
        date = st.date_input("Date")
        budget = st.number_input("Budget (DA)", min_value=0)

        if st.form_submit_button("VALIDER LE DOSSIER"):
            st.balloons()
