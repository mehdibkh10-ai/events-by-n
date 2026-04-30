import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EVENT PRO SYSTEM", layout="wide")

st.markdown("""
<style>
.stApp { background:#fff; color:#000; }
[data-testid="stSidebar"] { background:#f5f5f5; }
h1,h2,h3 { font-family: Arial; }
.stButton>button { background:#000; color:#fff; }
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)

def load(name):
    try:
        return conn.read(worksheet=name, ttl=0)
    except:
        return pd.DataFrame()

def save(name, df):
    conn.write(worksheet=name, data=df)  # 🔥 stable version

# =========================
# MENU
# =========================
with st.sidebar:
    st.title("⚜ EVENT PRO")
    page = st.radio("MENU", [
        "📦 INVENTAIRE",
        "📅 ÉVÉNEMENTS",
        "👥 CLIENTS",
        "📊 DASHBOARD"
    ])

# =========================================================
# 📦 INVENTAIRE
# =========================================================
if page == "📦 INVENTAIRE":

    st.header("📦 Gestion Stock Pro")

    inv = load("Inventaire")

    categories = [
        "Mobilier",
        "Textile",
        "Vaisselle",
        "Décoration",
        "Lumière",
        "Technique"
    ]

    if not inv.empty:
        for cat in categories:
            st.subheader(cat)

            dfc = inv[inv["Categorie"] == cat]

            for _, r in dfc.iterrows():
                achat = float(r["Prix_Achat"])
                loc = achat / 4
                valeur = loc * float(r["Stock"])

                st.write(f"""
                🔹 **{r['Article']}**
                - Stock: {r['Stock']}
                - Achat: {achat:.0f} DA
                - Location: {loc:.0f} DA
                - Valeur stock: {valeur:.0f} DA
                """)
                st.markdown("---")

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

                st.success("✅ Article ajouté")

# =========================================================
# 📅 ÉVÉNEMENTS
# =========================================================
elif page == "📅 ÉVÉNEMENTS":

    st.header("📅 Gestion Événements PRO")

    inv = load("Inventaire")
    events = load("Evenements")

    type_ev = st.selectbox("Type événement", ["Mariage", "Anniversaire", "Dîner", "Entreprise"])

    with st.form("event"):

        nom_event = st.text_input("Nom événement")
        date = st.date_input("Date")
        lieu = st.text_input("Lieu")

        # =========================
        # CLIENT LOGIC
        # =========================
        if type_ev == "Mariage":
            st.subheader("👰🤵 Clients Mariage")

            c1, c2 = st.columns(2)
            mari = c1.text_input("Nom Marié")
            mari_t = c1.text_input("Tel Marié")
            mariee = c2.text_input("Nom Mariée")
            mariee_t = c2.text_input("Tel Mariée")

        elif type_ev == "Anniversaire":
            st.subheader("🎂 Client Anniversaire")

            c1, c2 = st.columns(2)
            client = c1.text_input("Client")
            concerne = c2.text_input("Pour qui ?")
            tel = c1.text_input("Téléphone")

        else:
            st.subheader("👤 Client unique")
            client = st.text_input("Nom client")

        # =========================
        # ARTICLE
        # =========================
        article = st.selectbox("Article", inv["Article"].tolist() if not inv.empty else [])
        qty = st.number_input("Quantité", min_value=1)

        if st.form_submit_button("Créer événement"):

            row = inv[inv["Article"] == article]

            if not row.empty:

                prix_achat = float(row["Prix_Achat"].values[0])
                prix_loc = prix_achat / 4
                total = prix_loc * qty

                # EVENT SAVE
                new_event = pd.DataFrame([{
                    "Nom": nom_event,
                    "Type": type_ev,
                    "Date": date,
                    "Lieu": lieu,
                    "Article": article,
                    "Quantite": qty,
                    "Prix_Total": total
                }])

                events = pd.concat([events, new_event], ignore_index=True)
                save("Evenements", events)

                # STOCK UPDATE
                inv.loc[inv["Article"] == article, "Stock"] -= qty
                save("Inventaire", inv)

                st.success(f"""
                ✅ ÉVÉNEMENT CRÉÉ
                💰 Location/unité: {prix_loc:.0f} DA
                💵 Total: {total:.0f} DA
                📉 Stock mis à jour
                """)

# =========================================================
# 👥 CLIENTS
# =========================================================
elif page == "👥 CLIENTS":

    st.header("👥 Base Clients")

    st.info("Les clients sont enregistrés via les événements")

    events = load("Evenements")

    if not events.empty:
        st.dataframe(events)

# =========================================================
# 📊 DASHBOARD
# =========================================================
else:

    st.header("📊 Dashboard Rentabilité")

    inv = load("Inventaire")
    events = load("Evenements")

    if not inv.empty:
        total_stock = (inv["Stock"] * inv["Prix_Achat"]).sum()
        st.metric("💰 Valeur stock total", f"{total_stock:.0f} DA")

    if not events.empty:
        revenue = events["Prix_Total"].sum()
        st.metric("📈 Chiffre d'affaires", f"{revenue:.0f} DA")

        st.dataframe(events)
