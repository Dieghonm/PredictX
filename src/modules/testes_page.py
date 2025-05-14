import streamlit as st
import pandas as pd

def _setup_page_config():
    """Configurações de estilo da página."""
    st.markdown("""
        <style>
            .stButton>button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

def mostrar():
    st.title("📊 Visualização da Planilha")
    _setup_page_config()
    
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(100))

    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para a aba **Data**.")