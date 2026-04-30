import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Test Connexion Events by N")

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(ttl=0)
    st.write("✅ Connexion réussie ! Voici tes données :")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Erreur : {e}")
