import streamlit as st
import pandas as pd

def mostrar():
    st.title("📂 Escolha dos Dados")

    uploaded_file = st.file_uploader("📤 Upload CSV", type="csv")

    if st.button("📁 Usar arquivo de demonstração"):
        try:
            df = pd.read_feather("data/credit_scoring.ftr")
            st.session_state.df = df
            st.success("✅ Arquivo de demonstração carregado.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar exemplo: {e}")

    elif uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success("✅ Arquivo carregado com sucesso.")
        except Exception as e:
            st.error(f"❌ Erro ao ler o CSV: {e}")

    # Mostrar dados se já tiver carregado
    if st.session_state.get("df") is not None:
        st.subheader("📄 Visualização dos Dados Carregados")
        st.dataframe(st.session_state.df.head(5))

