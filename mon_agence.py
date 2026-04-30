import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import hashlib

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EVENT SaaS PRO", layout="wide")

st.markdown("""
<style>
.stApp { background:#F5F7FB; color:#000; }

[data-testid="stSidebar"] {
    background:#111827;
}

[data-testid="stSidebar"] * {
    color:white !important;
}

h1,h2,h3 {
    color:#111827;
}

.stButton>button {
    background:#2563EB !important;
    color:white !important;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB CONNECTION
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
# AUTH SYSTEM (SIMPLE SAAS LOGIN)
# =========================
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("🔐 EVENT SaaS LOGIN")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")

    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("⚜ EVENT SaaS PRO")

    page = st.radio("Navigation", [
        "📊 Dashboard",
        "📦 Inventaire",
        "📅 Événements",
        "👥 Clients"
    ])

# =========================
# LOAD DATA
# =========================
inv = load("Inventaire")
ev = load("Evenements")

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "📊 Dashboard":

    st.title("📊 Dashboard SaaS")

    col1, col2, col3 = st.columns(3)

    stock_value = 0
    if not inv.empty:
        stock_value = (inv["Stock"] * inv["Prix_Achat"]).sum()

    revenue = 0
    if not ev.empty:
        revenue = ev["Prix_Total"].sum()

    col1.metric("💰 Valeur stock", f"{stock_value:.0f} DA")
    col2.metric("📈 Chiffre d'affaires", f"{revenue:.0f} DA")
    col3.metric("📅 Événements", len(ev) if not ev.empty else 0)

    st.divider()

    if not ev.empty:
        st.subheader("📅 Derniers événements")
        st.dataframe(ev.tail(10))

# =========================================================
# 📦 INVENTAIRE
# =========================================================
elif page == "📦 Inventaire":

    st.title("📦 Gestion Stock")

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
                        box-shadow:0 2px 10px rgba(0,0,0,0.05);
                    ">
                        <b>🔹 {r['Article']}</b><br>
                        Stock: {r['Stock']}<br>
                        Achat: {achat:.0f} DA<br>
                        Location: <b>{loc:.0f} DA</b>
                    </div>
                    """, unsafe_allow_html=True)

    # ADD ITEM
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

    type_ev = st.selectbox("Type", ["Mariage", "Anniversaire", "Dîner", "Entreprise"])

    with st.form("event"):

        nom = st.text_input("Nom événement")
        date = st.date_input("Date")
        lieu = st.text_input("Lieu")

        article = st.selectbox("Article", inv["Article"].tolist() if not inv.empty else [])
        qty = st.number_input("Quantité", min_value=1)

        if st.form_submit_button("Créer événement"):

            row = inv[inv["Article"] == article]

            if not row.empty:

                prix = float(row["Prix_Achat"].values[0])
                loc = prix / 4
                total = loc * qty

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

                st.success("✅ Événement créé avec succès")

# =========================================================
# 👥 CLIENTS
# =========================================================
else:

    st.title("👥 Base Clients")

    if not ev.empty:
        st.dataframe(ev)
    else:
        st.info("Aucun client enregistré")
