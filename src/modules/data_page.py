import streamlit as st
import pandas as pd
import io
from pathlib import Path

def mostrar():
    st.title("📂 Escolha dos Dados")

    # Função para carregar arquivos de forma segura
    def carregar_arquivo(caminho, formato):
        try:
            caminho_completo = Path("data") / caminho
            if not caminho_completo.exists():
                raise FileNotFoundError(f"Arquivo {caminho} não encontrado na pasta data")
            
            if formato == "csv":
                return pd.read_csv(caminho_completo)
            elif formato == "xls":
                return pd.read_excel(caminho_completo, engine='xlwt')
            elif formato == "json":
                return pd.read_json(caminho_completo)
            elif formato == "parquet":
                return pd.read_parquet(caminho_completo)
            elif formato == "feather":
                return pd.read_feather(caminho_completo)
        except Exception as e:
            st.error(f"Erro ao carregar {caminho}: {str(e)}")
            return None

    # Upload de arquivo original
    uploaded_file = st.file_uploader(
        "📤 Upload de Arquivo",
        type=["csv", "xlsx", "xls", "json", "feather", "parquet"],
        help="Formatos suportados: CSV, Excel (xlsx, xls), JSON, Feather, Parquet"
    )

    if uploaded_file is not None:
        try:
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            elif file_name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            elif file_name.endswith('.feather') or file_name.endswith('.ftr'):
                df = pd.read_feather(uploaded_file)
            elif file_name.endswith('.parquet'):
                df = pd.read_parquet(uploaded_file)
            else:
                st.error("Formato de arquivo não suportado")
                return
            
            st.session_state.df = df
            st.success(f"✅ Arquivo {uploaded_file.name} carregado com sucesso.")
        except Exception as e:
            st.error(f"❌ Erro ao ler o arquivo: {e}")

    if st.button("📁 Usar arquivo de demonstração"):
        try:
            df = pd.read_feather("data/credit_scoring.ftr")
            st.session_state.df = df
            st.success("✅ Arquivo de demonstração carregado.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar exemplo: {e}")

    # Mostrar dados se já tiver carregado
    if st.session_state.get("df") is not None:
        st.subheader("📄 Visualização dos Dados Carregados")
        st.dataframe(st.session_state.df.head(5))