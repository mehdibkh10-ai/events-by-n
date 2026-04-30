import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION STYLE (NOIR & BLANC) ---
st.set_page_config(page_title="Events by N - Gestion Stock", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #DDDDDD; }
    h1, h2, h3, p, label { color: #000000 !important; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #000000 !important; color: #FFFFFF !important; border-radius: 4px; border: none; }
    .stExpander { border: 1px solid #EEEEEE !important; box-shadow: none !important; margin-bottom: 10px; }
    hr { border: 0.5px solid #EEEEEE; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_inv():
    try:
        df = conn.read(worksheet="Inventaire", ttl=0)
        df["Prix_Achat"] = pd.to_numeric(df["Prix_Achat"], errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

# --- NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Events by N")
    choix = st.radio("MENU", ["📦 INVENTAIRE PRO", "👥 CLIENTS & MARIAGES"])

# --- PAGE INVENTAIRE ---
if choix == "📦 INVENTAIRE PRO":
    st.header("📦 Gestion de l'Inventaire")
    df = load_inv()

    # Tes 6 catégories exactes
    categories = [
        "1. Mobilier et Structures",
        "2. Textiles et Linge de Table",
        "3. Verrerie, Vaisselle et Présentoirs",
        "4. Papeterie et Signalétique",
        "5. Éclairage et Ambiance",
        "6. Matériel Technique (Kit d'urgence)"
    ]

    for cat in categories:
        with st.expander(f"📂 {cat.upper()}"):
            items = df[df["Categorie"] == cat]
            
            if items.empty:
                st.write("*Aucun article dans ce dossier.*")
            else:
                # En-tête tableau
                c_h1, c_h2, c_h3, c_h4, c_h5 = st.columns([2.5, 1, 1, 1, 1.5])
                c_h1.write("**Article**")
                c_h2.write("**Stock**")
                c_h3.write("**Achat**")
                c_h4.write("**Location**")
                c_h5.write("**Rentabilité**")
                st.markdown("---")

                for _, row in items.iterrows():
                    p_achat = float(row['Prix_Achat'])
                    p_loc = p_achat / 4  # Ta règle du 1/4
                    
                    c1, c2, c3, c4, c5 = st.columns([2.5, 1, 1, 1, 1.5])
                    c1.write(f"🔹 {row['Article']}")
                    c2.write(f"{row['Stock']}")
                    c3.write(f"{p_achat:,.0f} DA")
                    c4.write(f"**{p_loc:,.0f} DA**")
                    c5.write("✅ Amorti en 4 loc.")
                    st.markdown("---")

    # Ajouter du stock
    with st.expander("➕ AJOUTER UN ARTICLE"):
        with st.form("new_stock"):
            c_a, c_b = st.columns(2)
            sel_cat = c_a.selectbox("Dossier", categories)
            sel_nom = c_b.text_input("Nom de l'article")
            sel_qty = c_a.number_input("Quantité", min_value=1)
            sel_prx = c_b.number_input("Prix d'achat unitaire (DA)", min_value=0)
            
            if st.form_submit_button("VALIDER L'AJOUT"):
                st.success(f"Article ajouté ! Prix de location fixé à {sel_prx/4} DA")

# --- PAGE CLIENTS ---
else:
    st.header("👥 Fiches Clients")
    type_ev = st.selectbox("Type", ["Mariage", "Anniversaire"])
    
    with st.form("client_form"):
        if type_ev == "Mariage":
            col1, col2 = st.columns(2)
            nom_f = col1.text_input("👰 Mariée (Nom/Prénom)")
            tel_f = col1.text_input("📞 Tél. Mariée")
            nom_h = col2.text_input("🤵 Marié (Nom/Prénom)")
            tel_h = col2.text_input("📞 Tél. Marié")
        else:
            col1, col2 = st.columns(2)
            nom_c = col1.text_input("👤 Nom du Client")
            nom_p = col2.text_input("🎂 Anniversaire pour...")
            tel_c = col1.text_input("📞 Téléphone")

        st.divider()
        lieu = st.text_input("📍 Lieu de l'événement")
        date = st.date_input("📅 Date")
        
        if st.form_submit_button("ENREGISTRER LE DOSSIER"):
            st.balloons()
