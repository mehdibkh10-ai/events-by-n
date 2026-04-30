import streamlit as st
import pandas as pd
import uuid
from datetime import date

# =========================
# CONFIG SITE SAAS
# =========================
st.set_page_config(
    page_title="EVENT SaaS | Enterprise",
    layout="wide",
    page_icon="💼"
)

# =========================
# DESIGN SAAS PRO
# =========================
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background-color: #F4F6FA;
    color: #111827;
    font-family: Arial;
}

/* SIDEBAR SAAS */
[data-testid="stSidebar"] {
    background: #0F172A;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* TITRES */
h1,h2,h3 {
    color:#0F172A !important;
}

/* BUTTONS */
.stButton>button {
    background:#2563EB !important;
    color:white !important;
    border-radius:10px;
    padding:8px 16px;
    border:none;
}

/* CARDS */
.card {
    background:white;
    padding:16px;
    border-radius:14px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
    margin-bottom:12px;
}

/* METRICS */
[data-testid="stMetricValue"] {
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE (SAAS LOCAL)
# =========================
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=[
        "Category", "Article", "Stock", "Purchase_Price"
    ])

if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=[
        "Event_ID",
        "Client_Name",
        "Client_Phone",
        "Client_Email",
        "Event_Type",
        "Start_Date",
        "End_Date",
        "Article",
        "Quantity",
        "Client_Budget",
        "Internal_Cost",
        "Total_Revenue",
        "Observation"
    ])

inv = st.session_state.inventory
events = st.session_state.events

# =========================
# SIDEBAR (SITE NAVIGATION)
# =========================
with st.sidebar:
    st.title("💼 EVENT SaaS")

    menu = st.radio("Navigation", [
        "📊 Dashboard",
        "📦 Inventory",
        "📅 Events",
        "👤 Clients"
    ])

# =========================================================
# 📊 DASHBOARD (BUSINESS VIEW)
# =========================================================
if menu == "📊 Dashboard":

    st.title("📊 Business Dashboard")

    total_revenue = events["Client_Budget"].sum() if not events.empty else 0
    total_cost = events["Internal_Cost"].sum() if not events.empty else 0
    profit = total_revenue - total_cost

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Revenue", f"{total_revenue:.0f} DA")
    col2.metric("💸 Cost", f"{total_cost:.0f} DA")
    col3.metric("📈 Profit", f"{profit:.0f} DA")

    st.divider()

    st.subheader("📅 Recent Events")
    st.dataframe(events.tail(10))

# =========================================================
# 📦 INVENTORY (SAAS STYLE)
# =========================================================
elif menu == "📦 Inventory":

    st.title("📦 Inventory Management")

    if inv.empty:
        st.info("No items in stock yet")
    else:
        for _, r in inv.iterrows():

            purchase = float(r["Purchase_Price"])
            rental = purchase / 4
            value = purchase * r["Stock"]

            st.markdown(f"""
            <div class="card">
                <h4>🔹 {r['Article']}</h4>
                <p>
                📂 Category: {r['Category']}<br>
                📦 Stock: <b>{r['Stock']}</b><br>
                💰 Purchase: {purchase:.0f} DA<br>
                📤 Rental: {rental:.0f} DA<br>
                📊 Stock Value: {value:.0f} DA
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("➕ Add Item")

    c1, c2 = st.columns(2)

    category = c1.text_input("Category")
    article = c2.text_input("Article")
    stock = c1.number_input("Stock", min_value=1)
    price = c2.number_input("Purchase Price", min_value=0)

    if st.button("Add Item"):

        new_item = pd.DataFrame([{
            "Category": category,
            "Article": article,
            "Stock": stock,
            "Purchase_Price": price
        }])

        st.session_state.inventory = pd.concat([inv, new_item], ignore_index=True)
        st.success("Item added")

# =========================================================
# 📅 EVENTS (CORE SAAS MODULE)
# =========================================================
elif menu == "📅 Events":

    st.title("📅 Event Management System")

    event_type = st.selectbox("Event Type", [
        "Wedding", "Birthday", "Corporate"
    ])

    st.subheader("👤 Client Information")

    c1, c2 = st.columns(2)

    client_name = c1.text_input("Client Name")
    client_phone = c1.text_input("Phone")
    client_email = c2.text_input("Email")

    st.divider()

    st.subheader("📅 Event Details")

    event_name = st.text_input("Event Name")

    col1, col2 = st.columns(2)

    start_date = col1.date_input("Start Date", value=date.today())
    end_date = col2.date_input("End Date", value=date.today())

    article = st.text_input("Article")
    qty = st.number_input("Quantity", min_value=1)

    client_budget = st.number_input("💰 Client Budget", min_value=0)
    internal_cost = st.number_input("💸 Internal Cost", min_value=0)

    observation = st.text_area("Observation")

    if st.button("Create Event"):

        if not inv.empty and article in inv["Article"].values:

            event_id = str(uuid.uuid4())[:8]

            purchase = float(inv[inv["Article"] == article]["Purchase_Price"].values[0])
            rental = purchase / 4
            revenue = rental * qty

            new_event = pd.DataFrame([{
                "Event_ID": event_id,
                "Client_Name": client_name,
                "Client_Phone": client_phone,
                "Client_Email": client_email,
                "Event_Type": event_type,
                "Start_Date": start_date,
                "End_Date": end_date,
                "Article": article,
                "Quantity": qty,
                "Client_Budget": client_budget,
                "Internal_Cost": internal_cost,
                "Total_Revenue": revenue,
                "Observation": observation
            }])

            st.session_state.events = pd.concat([events, new_event], ignore_index=True)

            # stock update safe
            inv.loc[inv["Article"] == article, "Stock"] -= qty
            st.session_state.inventory = inv

            st.success(f"""
            ✅ EVENT CREATED
            🆔 ID: {event_id}
            💰 Revenue: {revenue:.0f} DA
            📅 {start_date} → {end_date}
            """)

        else:
            st.error("Article not found")

# =========================================================
# 👤 CLIENTS (AUTO GENERATED)
# =========================================================
else:

    st.title("👤 Clients Database")

    if not events.empty:

        clients_df = events[[
            "Client_Name",
            "Client_Phone",
            "Client_Email",
            "Event_Type",
            "Event_ID"
        ]]

        st.dataframe(clients_df)

        st.subheader("🔍 Search Client")
        search = st.text_input("Search by name")

        if search:
            st.dataframe(
                clients_df[clients_df["Client_Name"].str.contains(search, case=False)]
            )
    else:
        st.info("No clients yet")
