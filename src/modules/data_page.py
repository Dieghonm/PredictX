import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional, Union

# Configurações de tipos
DataFrame = pd.DataFrame
FileUploader = st.runtime.uploaded_file_manager.UploadedFile
PathLike = Union[str, Path]

def mostrar():
    """Página principal para carregamento de dados na aplicação de Scoragem de Crédito."""
    st.title("📂 Escolha dos Dados")
    _setup_page_config()
    _handle_data_loading()

def _setup_page_config():
    """Configurações adicionais da página."""
    st.markdown("""
        <style>
            .stButton>button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

def _handle_data_loading():
    """Gerencia todo o processo de carregamento de dados."""
    _handle_file_upload()
    _handle_demo_file()
    _display_loaded_data()

def _handle_file_upload():
    """Processa o upload de arquivos pelo usuário."""
    uploaded_file = st.file_uploader(
        "📤 Upload de Arquivo",
        type=["csv", "xlsx", "xls", "json", "feather", "parquet"],
        help="Formatos suportados: CSV, Excel (xlsx, xls), JSON, Feather, Parquet"
    )

    if uploaded_file:
        df = _load_uploaded_file(uploaded_file)
        if df is not None:
            st.session_state.df = df
            st.success(f"✅ Arquivo {uploaded_file.name} carregado com sucesso.")

def _load_uploaded_file(uploaded_file: FileUploader) -> Optional[DataFrame]:
    """Carrega um arquivo enviado pelo usuário."""
    file_name = uploaded_file.name.lower()
    file_mapping = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.json': pd.read_json,
        '.feather': pd.read_feather,
        '.ftr': pd.read_feather,
        '.parquet': pd.read_parquet
    }

    for ext, loader in file_mapping.items():
        if file_name.endswith(ext):
            try:
                return loader(uploaded_file)
            except Exception as e:
                st.error(f"❌ Erro ao ler o arquivo {file_name}: {str(e)}")
                return None

    st.error("Formato de arquivo não suportado")
    return None

def _handle_demo_file():
    """Carrega o arquivo de demonstração quando solicitado."""
    if st.button("📁 Usar arquivo de demonstração", help="Carrega dados de exemplo para teste"):
        demo_file = Path("data/credit_scoring.ftr")
        try:
            if not demo_file.exists():
                raise FileNotFoundError(f"Arquivo de demonstração não encontrado em {demo_file}")
            
            df = pd.read_feather(demo_file)
            st.session_state.df = df
            st.success("✅ Arquivo de demonstração carregado.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar exemplo: {e}")

def _display_loaded_data():
    """Exibe os dados carregados se estiverem disponíveis."""
    if "df" in st.session_state and st.session_state.df is not None:
        st.subheader("📄 Visualização dos Dados Carregados")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Total de Registros", len(st.session_state.df))
            st.metric("Total de Colunas", len(st.session_state.df.columns))
        
        with col2:
            st.dataframe(
                st.session_state.df.head(5),
                use_container_width=True,
                height=210
            )