import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="EVENT SaaS PRO", layout="wide")

# =========================
# STYLE CLEAN + LISIBLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F3F4F6;
    color: #111111;
}

h1, h2, h3, h4, p, label {
    color: #111111 !important;
}

/* sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* buttons */
.stButton>button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 10px;
}

/* cards */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    color: #111;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA LOCAL (SAFE MODE)
# =========================
if "inv" not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["Categorie", "Article", "Stock", "Prix_Achat"])

if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=[
        "Nom", "Type", "Article", "Quantite", "Prix_Total"
    ])

inv = st.session_state.inv
events = st.session_state.events

# =========================
# SIDEBAR
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

    st.title("📊 Dashboard SaaS")

    col1, col2, col3 = st.columns(3)

    stock_value = (inv["Stock"] * inv["Prix_Achat"]).sum() if not inv.empty else 0
    revenue = events["Prix_Total"].sum() if not events.empty else 0

    col1.metric("💰 Valeur stock", f"{stock_value:.0f} DA")
    col2.metric("📈 Chiffre d'affaires", f"{revenue:.0f} DA")
    col3.metric("📦 Articles", len(inv))

    st.divider()

    st.subheader("📅 Derniers événements")
    st.dataframe(events.tail(10) if not events.empty else events)

# =========================================================
# 📦 INVENTAIRE
# =========================================================
elif page == "📦 Inventaire":

    st.title("📦 Inventaire")

    # AFFICHAGE
    for i, row in inv.iterrows():

        achat = float(row["Prix_Achat"])
        loc = achat / 4

        st.markdown(f"""
        <div class="card">
            <b>{row['Article']}</b><br>
            Catégorie: {row['Categorie']}<br>
            Stock: {row['Stock']}<br>
            Achat: {achat:.0f} DA<br>
            Location: <b>{loc:.0f} DA</b>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # AJOUT
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
# 📅 ÉVÉNEMENTS
# =========================================================
else:

    st.title("📅 Événements")

    type_ev = st.selectbox("Type", ["Mariage", "Anniversaire", "Entreprise"])

    nom = st.text_input("Nom événement")
    article = st.text_input("Article utilisé")
    qty = st.number_input("Quantité", min_value=1)

    if st.button("Créer événement"):

        if not inv.empty and article in inv["Article"].values:

            price = float(inv[inv["Article"] == article]["Prix_Achat"].values[0])
            loc = price / 4
            total = loc * qty

            new_ev = pd.DataFrame([{
                "Nom": nom,
                "Type": type_ev,
                "Article": article,
                "Quantite": qty,
                "Prix_Total": total
            }])

            st.session_state.events = pd.concat([events, new_ev], ignore_index=True)

            # update stock
            inv.loc[inv["Article"] == article, "Stock"] -= qty
            st.session_state.inv = inv

            st.success(f"✅ Événement créé | Total: {total:.0f} DA")

        else:
            st.error("Article introuvable")

    st.divider()

    st.subheader("📋 Liste événements")
    st.dataframe(events)
