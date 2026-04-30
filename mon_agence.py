import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- STYLE ---
st.set_page_config(page_title="Events by N - Gestion Pro", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #FFFFFF; color: #000000; }
[data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #DDDDDD; }
h1, h2, h3, p, label { color: #000000 !important; font-family: Arial; }
.stButton>button { background-color: #000000 !important; color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- CONNEXION GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOAD INVENTAIRE ---
def load_inv():
    try:
        df = conn.read(worksheet="Inventaire", ttl=0)
        df["Prix_Achat"] = pd.to_numeric(df["Prix_Achat"], errors="coerce").fillna(0)
        return df
    except:
        return pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

# --- LOAD EVENTS ---
def load_events():
    try:
        return conn.read(worksheet="Evenements", ttl=0)
    except:
        return pd.DataFrame(columns=[
            "Nom", "Type", "Date", "Lieu", "Article", "Quantite", "Prix_Total"
        ])

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚜️ Events by N")
    choix = st.radio("MENU", [
        "📦 INVENTAIRE PRO",
        "👥 CLIENTS",
        "📅 ÉVÉNEMENTS"
    ])

# =========================================================
# 📦 INVENTAIRE
# =========================================================
if choix == "📦 INVENTAIRE PRO":
    st.header("📦 Gestion Inventaire")

    df = load_inv()

    categories = [
        "1. Mobilier et Structures",
        "2. Textiles et Linge de Table",
        "3. Verrerie, Vaisselle et Présentoirs",
        "4. Papeterie et Signalétique",
        "5. Éclairage et Ambiance",
        "6. Matériel Technique (Kit d'urgence)"
    ]

    for cat in categories:
        with st.expander(f"📂 {cat}"):
            items = df[df["Categorie"] == cat]

            if items.empty:
                st.write("Aucun article")
            else:
                for _, row in items.iterrows():
                    achat = float(row["Prix_Achat"])
                    loc = achat / 4

                    st.write(f"""
                    🔹 **{row['Article']}**  
                    Stock: {row['Stock']}  
                    Achat: {achat:.0f} DA  
                    Location: {loc:.0f} DA
                    """)
                    st.markdown("---")

    # ADD STOCK
    with st.expander("➕ Ajouter article"):
        with st.form("add_item"):
            col1, col2 = st.columns(2)

            cat = col1.selectbox("Catégorie", categories)
            article = col2.text_input("Article")
            stock = col1.number_input("Stock", min_value=1)
            prix = col2.number_input("Prix achat", min_value=0)

            if st.form_submit_button("Ajouter"):
                st.success("Article ajouté (Google Sheets à connecter pour sauvegarde)")

# =========================================================
# 👥 CLIENTS
# =========================================================
elif choix == "👥 CLIENTS":
    st.header("👥 Gestion Clients")

    type_ev = st.selectbox("Type événement", ["Mariage", "Anniversaire"])

    with st.form("client"):
        if type_ev == "Mariage":
            c1, c2 = st.columns(2)
            nom1 = c1.text_input("Mariée")
            tel1 = c1.text_input("Téléphone Mariée")
            nom2 = c2.text_input("Marié")
            tel2 = c2.text_input("Téléphone Marié")
        else:
            c1, c2 = st.columns(2)
            nom = c1.text_input("Nom client")
            event = c2.text_input("Pour qui ?")
            tel = c1.text_input("Téléphone")

        lieu = st.text_input("Lieu")
        date = st.date_input("Date")

        if st.form_submit_button("Enregistrer"):
            st.success("Client enregistré")

# =========================================================
# 📅 ÉVÉNEMENTS
# =========================================================
else:
    st.header("📅 Gestion Événements")

    inv = load_inv()
    events = load_events()

    with st.form("event_form"):
        nom = st.text_input("Nom événement")
        type_ev = st.selectbox("Type", ["Mariage", "Anniversaire", "Entreprise", "Autre"])
        date = st.date_input("Date")
        lieu = st.text_input("Lieu")

        article = st.selectbox("Article", inv["Article"].unique() if not inv.empty else [])
        qty = st.number_input("Quantité", min_value=1)

        if st.form_submit_button("Créer événement"):

            row = inv[inv["Article"] == article]

            if not row.empty:
                prix_achat = float(row["Prix_Achat"].values[0])
                prix_loc = prix_achat / 4
                total = prix_loc * qty

                new_event = pd.DataFrame([{
                    "Nom": nom,
                    "Type": type_ev,
                    "Date": date,
                    "Lieu": lieu,
                    "Article": article,
                    "Quantite": qty,
                    "Prix_Total": total
                }])

                st.success(f"""
                ✅ Événement créé  
                📦 Article: {article}  
                💰 Prix location: {prix_loc:.0f} DA  
                💵 Total: {total:.0f} DA
                """)

                st.dataframe(new_event)

            else:
                st.error("Article introuvable")

    # LIST EVENTS
    st.subheader("📋 Liste événements")
    st.dataframe(events)
