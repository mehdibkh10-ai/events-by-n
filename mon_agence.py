import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =========================
# CONFIG UI MODERNE
# =========================
st.set_page_config(page_title="EVENT PRO SYSTEM", layout="wide")

st.markdown("""
<style>

/* Fond général */
.stApp {
    background-color: #F4F6F9;
    color: #000000;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1F2937;
    color: white;
}

/* Texte sidebar */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Titres */
h1, h2, h3 {
    color: #111827 !important;
    font-family: Arial;
}

/* Boutons */
.stButton>button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 8px 15px;
}

/* Cards style */
.block-container {
    padding: 2rem;
}

/* Inputs */
input, selectbox, textarea {
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)

def load(name):
    try:
        return conn.read(worksheet=name, ttl=0)
    except:
        return pd.DataFrame()

def save(name, df):
    conn.write(worksheet=name, data=df)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("⚜ EVENT PRO")
    page = st.radio("Navigation", [
        "📊 Dashboard",
        "📦 Inventaire",
        "📅 Événements",
        "👥 Clients"
    ])

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "📊 Dashboard":

    st.title("📊 Tableau de bord")

    inv = load("Inventaire")
    ev = load("Evenements")

    col1, col2, col3 = st.columns(3)

    stock_val = 0
    if not inv.empty:
        stock_val = (inv["Stock"] * inv["Prix_Achat"]).sum()

    revenue = 0
    if not ev.empty:
        revenue = ev["Prix_Total"].sum()

    col1.metric("💰 Valeur stock", f"{stock_val:.0f} DA")
    col2.metric("📈 CA total", f"{revenue:.0f} DA")
    col3.metric("📦 Articles", len(inv) if not inv.empty else 0)

# =========================================================
# 📦 INVENTAIRE
# =========================================================
elif page == "📦 Inventaire":

    st.title("📦 Gestion Inventaire")

    inv = load("Inventaire")

    categories = ["Mobilier", "Textile", "Vaisselle", "Décoration", "Lumière", "Technique"]

    if not inv.empty:
        for cat in categories:

            dfc = inv[inv["Categorie"] == cat]

            if not dfc.empty:
                st.subheader(f"📂 {cat}")

                for _, r in dfc.iterrows():

                    achat = float(r["Prix_Achat"])
                    loc = achat / 4

                    st.markdown(f"""
                    <div style="
                        background:white;
                        padding:15px;
                        border-radius:12px;
                        margin-bottom:10px;
                        box-shadow:0px 2px 8px rgba(0,0,0,0.05);
                        color:black;
                    ">
                        <b>🔹 {r['Article']}</b><br>
                        Stock: {r['Stock']}<br>
                        Achat: {achat:.0f} DA<br>
                        Location: <b>{loc:.0f} DA</b>
                    </div>
                    """, unsafe_allow_html=True)

    # ADD
    with st.expander("➕ Ajouter article"):
        with st.form("add"):

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

                inv = pd.concat([inv, new], ignore_index=True)
                save("Inventaire", inv)

                st.success("✅ Ajouté")

# =========================================================
# 📅 ÉVÉNEMENTS
# =========================================================
elif page == "📅 Événements":

    st.title("📅 Gestion Événements")

    inv = load("Inventaire")
    ev = load("Evenements")

    type_ev = st.selectbox("Type événement", ["Mariage", "Anniversaire", "Dîner", "Entreprise"])

    with st.form("event"):

        nom = st.text_input("Nom événement")
        date = st.date_input("Date")
        lieu = st.text_input("Lieu")

        article = st.selectbox("Article", inv["Article"].tolist() if not inv.empty else [])
        qty = st.number_input("Quantité", min_value=1)

        if st.form_submit_button("Créer"):

            row = inv[inv["Article"] == article]

            if not row.empty:

                prix_achat = float(row["Prix_Achat"].values[0])
                prix_loc = prix_achat / 4
                total = prix_loc * qty

                new_ev = pd.DataFrame([{
                    "Nom": nom,
                    "Type": type_ev,
                    "Date": date,
                    "Lieu": lieu,
                    "Article": article,
                    "Quantite": qty,
                    "Prix_Total": total
                }])

                ev = pd.concat([ev, new_ev], ignore_index=True)
                save("Evenements", ev)

                inv.loc[inv["Article"] == article, "Stock"] -= qty
                save("Inventaire", inv)

                st.success("✅ Événement créé")

# =========================================================
# 👥 CLIENTS
# =========================================================
else:

    st.title("👥 Clients")

    ev = load("Evenements")

    if not ev.empty:
        st.dataframe(ev)
    else:
        st.info("Aucun client")
