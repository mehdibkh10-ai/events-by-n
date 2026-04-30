import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Events by N", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #FFFFFF; color: #000000; }
[data-testid="stSidebar"] { background-color: #F8F9FA !important; }
h1,h2,h3,p,label { color:#000 !important; font-family:Arial; }
.stButton>button { background:#000 !important; color:#fff !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# CONNEXION GOOGLE SHEETS
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)

# =========================
# LOAD DATA
# =========================
def load_sheet(name):
    try:
        return conn.read(worksheet=name, ttl=0)
    except:
        return pd.DataFrame()

def save_sheet(name, df):
    conn.update(worksheet=name, data=df)

# =========================
# SIDEBAR MENU
# =========================
with st.sidebar:
    st.title("⚜️ Events by N")
    choix = st.radio("MENU", [
        "📦 INVENTAIRE",
        "👥 CLIENTS",
        "📅 ÉVÉNEMENTS"
    ])

# =========================================================
# 📦 INVENTAIRE
# =========================================================
if choix == "📦 INVENTAIRE":

    st.header("📦 Gestion Inventaire")

    inv = load_sheet("Inventaire")

    categories = [
        "Mobilier",
        "Textiles",
        "Vaisselle",
        "Papeterie",
        "Éclairage",
        "Technique"
    ]

    # -------------------------
    # AFFICHAGE
    # -------------------------
    if not inv.empty:
        for cat in categories:
            st.subheader(cat)

            df_cat = inv[inv["Categorie"] == cat]

            if df_cat.empty:
                st.write("Aucun article")
            else:
                for _, row in df_cat.iterrows():
                    achat = float(row["Prix_Achat"])
                    loc = achat / 4

                    st.write(f"""
                    🔹 {row['Article']}  
                    Stock: {row['Stock']}  
                    Achat: {achat:.0f} DA  
                    Location: {loc:.0f} DA
                    """)
                    st.markdown("---")

    # -------------------------
    # AJOUT ARTICLE
    # -------------------------
    with st.expander("➕ Ajouter article"):
        with st.form("add_inv"):
            c1, c2 = st.columns(2)

            cat = c1.selectbox("Catégorie", categories)
            article = c2.text_input("Article")
            stock = c1.number_input("Stock", min_value=1)
            prix = c2.number_input("Prix achat", min_value=0)

            if st.form_submit_button("Ajouter"):

                new = pd.DataFrame([{
                    "Categorie": cat,
                    "Article": article,
                    "Stock": stock,
                    "Prix_Achat": prix
                }])

                inv = load_sheet("Inventaire")
                inv = pd.concat([inv, new], ignore_index=True)

                save_sheet("Inventaire", inv)

                st.success("✅ Article ajouté en base")

# =========================================================
# 👥 CLIENTS
# =========================================================
elif choix == "👥 CLIENTS":

    st.header("👥 Clients")

    type_ev = st.selectbox("Type", ["Mariage", "Anniversaire"])

    with st.form("client"):

        if type_ev == "Mariage":
            c1, c2 = st.columns(2)
            nom1 = c1.text_input("Mariée")
            tel1 = c1.text_input("Tel Mariée")
            nom2 = c2.text_input("Marié")
            tel2 = c2.text_input("Tel Marié")
        else:
            c1, c2 = st.columns(2)
            nom = c1.text_input("Nom")
            tel = c2.text_input("Téléphone")

        lieu = st.text_input("Lieu")
        date = st.date_input("Date")

        if st.form_submit_button("Enregistrer"):
            st.success("✅ Client enregistré")

# =========================================================
# 📅 ÉVÉNEMENTS (BASE DE DONNÉES)
# =========================================================
else:

    st.header("📅 Événements")

    inv = load_sheet("Inventaire")
    events = load_sheet("Evenements")

    with st.form("event"):

        nom = st.text_input("Nom événement")
        type_ev = st.selectbox("Type", ["Mariage", "Anniversaire", "Entreprise"])
        date = st.date_input("Date")
        lieu = st.text_input("Lieu")

        article = st.selectbox(
            "Article",
            inv["Article"].tolist() if not inv.empty else []
        )

        qty = st.number_input("Quantité", min_value=1)

        if st.form_submit_button("Créer événement"):

            row = inv[inv["Article"] == article]

            if not row.empty:

                prix_achat = float(row["Prix_Achat"].values[0])
                prix_loc = prix_achat / 4
                total = prix_loc * qty

                # -------------------------
                # AJOUT EVENT
                # -------------------------
                new_event = pd.DataFrame([{
                    "Nom": nom,
                    "Type": type_ev,
                    "Date": date,
                    "Lieu": lieu,
                    "Article": article,
                    "Quantite": qty,
                    "Prix_Total": total
                }])

                events = pd.concat([events, new_event], ignore_index=True)
                save_sheet("Evenements", events)

                # -------------------------
                # DIMINUER STOCK
                # -------------------------
                inv.loc[inv["Article"] == article, "Stock"] -= qty
                save_sheet("Inventaire", inv)

                st.success(f"""
                ✅ Événement créé  
                💰 Location/unité: {prix_loc:.0f} DA  
                💵 Total: {total:.0f} DA  
                📉 Stock mis à jour
                """)

            else:
                st.error("Article introuvable")
