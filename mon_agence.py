import streamlit as st
import pandas as pd
import uuid
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EVENT SaaS PRO", layout="wide")

st.markdown("""
<style>
.stApp { background:#F3F4F6; color:#111; }

[data-testid="stSidebar"] {
    background:#111827;
}
[data-testid="stSidebar"] * {
    color:white !important;
}

h1,h2,h3 { color:#111 !important; }

.stButton>button {
    background:#2563EB !important;
    color:white !important;
    border-radius:10px;
}

.card {
    background:white;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB LOCAL
# =========================
if "inv" not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=[
        "Categorie", "Article", "Stock", "Prix_Achat"
    ])

if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=[
        "Event_ID",
        "Client",
        "Type",
        "Date_Debut",
        "Date_Fin",
        "Article",
        "Quantite",
        "Budget_Client",
        "Budget_Personnel",
        "Total",
        "Observation"
    ])

inv = st.session_state.inv
events = st.session_state.events

# =========================
# MENU
# =========================
with st.sidebar:
    st.title("⚜ EVENT SaaS")

    page = st.radio("Navigation", [
        "📊 Dashboard",
        "📦 Inventaire",
        "📅 Événements"
    ])

# =========================================================
# 📊 DASHBOARD
# =========================================================
if page == "📊 Dashboard":

    st.title("📊 Dashboard")

    total_client = events["Budget_Client"].sum() if not events.empty else 0
    total_cost = events["Budget_Personnel"].sum() if not events.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 CA Client", f"{total_client:.0f} DA")
    col2.metric("💸 Coût total", f"{total_cost:.0f} DA")
    col3.metric("📅 Events", len(events))

    st.divider()

    st.dataframe(events)

# =========================================================
# 📦 INVENTAIRE
# =========================================================
elif page == "📦 Inventaire":

    st.title("📦 Stock")

    for _, r in inv.iterrows():

        achat = float(r["Prix_Achat"])
        loc = achat / 4

        st.markdown(f"""
        <div class="card">
            <b>{r['Article']}</b><br>
            Catégorie: {r['Categorie']}<br>
            Stock: {r['Stock']}<br>
            Achat: {achat:.0f} DA<br>
            Location: {loc:.0f} DA
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("➕ Ajouter article")

    c1, c2 = st.columns(2)

    cat = c1.text_input("Catégorie")
    article = c2.text_input("Article")
    stock = c1.number_input("Stock", min_value=1)
    prix = c2.number_input("Prix achat", min_value=0)

    if st.button("Ajouter"):

        new = pd.DataFrame([{
            "Categorie": cat,
            "Article": article,
            "Stock": stock,
            "Prix_Achat": prix
        }])

        st.session_state.inv = pd.concat([inv, new], ignore_index=True)
        st.success("Ajouté")

# =========================================================
# 📅 ÉVÉNEMENTS (VERSION PRO COMPLETE)
# =========================================================
elif page == "📅 Événements":

    st.title("📅 Création événement PRO")

    type_ev = st.selectbox("Type événement", [
        "Mariage", "Anniversaire", "Entreprise"
    ])

    # CLIENT
    st.subheader("👤 Client")

    c1, c2 = st.columns(2)

    client = c1.text_input("Nom client")
    tel = c1.text_input("Téléphone")
    email = c2.text_input("Email")

    st.divider()

    # EVENT
    st.subheader("📅 Informations événement")

    nom_event = st.text_input("Nom événement")

    col1, col2 = st.columns(2)

    date_debut = col1.date_input("Date début", value=date.today())
    date_fin = col2.date_input("Date fin", value=date.today())

    article = st.text_input("Article")
    qty = st.number_input("Quantité", min_value=1)

    observation = st.text_area("Observation (notes client)")

    budget_client = st.number_input("💰 Budget client (DA)", min_value=0)

    budget_personnel = st.number_input("💸 Budget personnel (coût estimé)", min_value=0)

    if st.button("Créer événement"):

        if not inv.empty and article in inv["Article"].values:

            event_id = str(uuid.uuid4())[:8]

            price = float(inv[inv["Article"] == article]["Prix_Achat"].values[0])
            loc = price / 4
            total = loc * qty

            new_event = pd.DataFrame([{
                "Event_ID": event_id,
                "Client": client,
                "Type": type_ev,
                "Date_Debut": date_debut,
                "Date_Fin": date_fin,
                "Article": article,
                "Quantite": qty,
                "Budget_Client": budget_client,
                "Budget_Personnel": budget_personnel,
                "Total": total,
                "Observation": observation
            }])

            st.session_state.events = pd.concat([events, new_event], ignore_index=True)

            # stock update sécurisé
            inv.loc[inv["Article"] == article, "Stock"] -= qty
            st.session_state.inv = inv

            st.success(f"""
            ✅ EVENT CRÉÉ
            🆔 ID: {event_id}
            💰 Total: {total:.0f} DA
            📅 {date_debut} → {date_fin}
            """)

        else:
            st.error("Article introuvable")
