st.markdown("""
<style>

/* =========================
   BACKGROUND GLOBAL
========================= */
.stApp {
    background-color: #F3F4F6 !important;
    color: #111111 !important;
}

/* =========================
   TEXTE GLOBAL (FORCE NOIR)
========================= */
h1, h2, h3, h4, h5, p, span, label, div {
    color: #111111 !important;
}

/* =========================
   SIDEBAR (DARK PRO)
========================= */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* texte sidebar blanc (normal ici) */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* =========================
   BOUTONS
========================= */
.stButton>button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 10px;
    border: none;
}

/* =========================
   INPUTS
========================= */
input, textarea, select {
    background-color: white !important;
    color: #111111 !important;
    border-radius: 8px !important;
    border: 1px solid #D1D5DB !important;
}

/* =========================
   CARDS PRO
========================= */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    color: #111111 !important;
}

</style>
""", unsafe_allow_html=True)
