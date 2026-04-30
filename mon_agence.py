import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EVENT SaaS PRO", layout="wide")

# =========================
# STYLE PRO
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F3F4F6;
    color: #111;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Titles */
h1,h2,h3,h4,p,label {
    color: #111 !important;
}

/* Buttons */
.stButton>button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 10px;
}

/* Cards */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION DB (LOCAL SAFE)
# =========================
if "inv" not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=[
        "Categorie", "Article", "Stock", "Prix_Achat"
    ])

if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=[
        "Nom", "Type", "Client", "Article", "Quantite", "Prix_Total"
    ])

if "clients" not in st.session_state:
    st.session_state.clients = pd.DataFrame(columns=[
        "Nom", "Telephone", "Email", "Type", "Evenement"
    ])

inv = st.session_state.inv
events = st.session_state.events
clients = st.session_state.clients

# =========================
# MENU
# =========================
with st.sidebar:
    st.title("⚜ EVENT SaaS")

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

    st.title("📊 Dashboard SaaS")

    stock_value = (inv["Stock"] * inv["Prix_Achat"]).sum() if not inv.empty else 0
    revenue = events["Prix_Total"].sum() if not events.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Valeur stock", f"{stock_value:.0f} DA")
    col2.metric("📈 CA total", f"{revenue:.0f} DA")
    col3.metric("👥 Clients", len(clients))

    st.divider()

    st.subheader("📅 Derniers événements")
    st.dataframe(events.tail(10) if not events.empty else events)

# =========================================================
# 📦 INVENTAIRE (VERSION PRO AMÉLIORÉE)
# =========================================================
elif page == "📦 Inventaire":

    st.title("📦 Gestion Inventaire PRO")

    if inv.empty:
        st.info("Aucun article dans le stock")
    else:

        # =========================
        # TABLEAU PRO
        # =========================
        st.subheader("📊 Vue globale")

        display = inv.copy()
        display["Prix_Location"] = display["Prix_Achat"] / 4
        display["Valeur_Stock"] = display["Stock"] * display["Prix_Achat"]

        st.dataframe(display, use_container_width=True)

        st.divider()

        # =========================
        # CARDS MODERNES
        # =========================
        st.subheader("📦 Détails articles")

        for _, r in inv.iterrows():

            achat = float(r["Prix_Achat"])
            loc = achat / 4
            valeur = float(r["Stock"]) * achat

            st.markdown(f"""
            <div class="card">
                <h4>🔹 {r['Article']}</h4>
                <p>
                📂 Catégorie: <b>{r['Categorie']}</b><br>
                📦 Stock: <b>{r['Stock']}</b><br>
                💰 Achat: <b>{achat:.0f} DA</b><br>
                📤 Location: <b>{loc:.0f} DA</b><br>
                📊 Valeur stock: <b>{valeur:.0f} DA</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # =========================
    # AJOUT ARTICLE
    # =========================
    st.subheader("➕ Ajouter article")

    c1, c2 = st.columns(2)

    cat = c1.text_input("Catégorie")
    article = c2.text_input("Article")
    stock = c1.number_input("Stock", min_value=1)
    prix = c2.number_input("Prix achat", min_value=0)

    if st.button("Ajouter article"):

        new = pd.DataFrame([{
            "Categorie": cat,
            "Article": article,
            "Stock": stock,
            "Prix_Achat": prix
        }])

        st.session_state.inv = pd.concat([inv, new], ignore_index=True)

        st.success("✅ Article ajouté")

# =========================================================
# 📅 ÉVÉNEMENTS (AVEC CLIENTS)
# =========================================================
elif page == "📅 Événements":

    st.title("📅 Gestion Événements")

    type_ev = st.selectbox("Type événement", [
        "Mariage", "Anniversaire", "Entreprise"
    ])

    st.subheader("👤 Client")

    c1, c2 = st.columns(2)

    nom_client = c1.text_input("Nom client")
    tel = c1.text_input("Téléphone")
    email = c2.text_input("Email")

    st.divider()

    nom_event = st.text_input("Nom événement")
    article = st.text_input("Article")
    qty = st.number_input("Quantité", min_value=1)

    if st.button("Créer événement"):

        if not inv.empty and article in inv["Article"].values:

            price = float(inv[inv["Article"] == article]["Prix_Achat"].values[0])
            loc = price / 4
            total = loc * qty

            # EVENT
            new_event = pd.DataFrame([{
                "Nom": nom_event,
                "Type": type_ev,
                "Client": nom_client,
                "Article": article,
                "Quantite": qty,
                "Prix_Total": total
            }])

            st.session_state.events = pd.concat([events, new_event], ignore_index=True)

            # CLIENT
            new_client = pd.DataFrame([{
                "Nom": nom_client,
                "Telephone": tel,
                "Email": email,
                "Type": type_ev,
                "Evenement": nom_event
            }])

            st.session_state.clients = pd.concat([
                clients,
                new_client
            ], ignore_index=True)

            # STOCK UPDATE
            inv.loc[inv["Article"] == article, "Stock"] -= qty
            st.session_state.inv = inv

            st.success(f"✅ Événement créé | Total: {total:.0f} DA")

        else:
            st.error("Article introuvable")

    st.divider()

    st.subheader("📋 Liste événements")
    st.dataframe(events)

# =========================================================
# 👥 CLIENTS
# =========================================================
else:

    st.title("👥 Base Clients")

    if not clients.empty:
        st.dataframe(clients)

        st.subheader("🔍 Recherche client")
        search = st.text_input("Nom client")

        if search:
            st.dataframe(
                clients[clients["Nom"].str.contains(search, case=False)]
            )
    else:
        st.info("Aucun client enregistré")
