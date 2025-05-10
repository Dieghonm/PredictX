import streamlit as st
import pandas as pd

def mostrar():
    st.title("📈 Gráficos (em breve)")
    if st.session_state.df is not None:
        st.write("Você poderá criar gráficos com os dados aqui.")
    else:
        st.warning("⚠️ Carregue os dados na aba **Data**.")