import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional, Union

# Configurações de tipos
DataFrame = pd.DataFrame
FileUploader = st.runtime.uploaded_file_manager.UploadedFile
PathLike = Union[str, Path]

# Configuração dos datasets de demonstração
DEMO_FILES = {
    "credit_scoring": {
        "path": Path("data/credit_scoring.ftr"),
        "name": "Credit Scoring",
        "description": "Dataset para análise de risco de crédito",
        "icon": "💳",
        "loader": pd.read_feather
    },
    "hypertension": {
        "path": Path("data/hypertension_dataset.csv"),
        "name": "Hipertensão",
        "description": "Dataset médico para predição de hipertensão",
        "icon": "🏥",
        "loader": pd.read_csv
    },
    "teen_addiction": {
        "path": Path("data/teen_phone_addiction_dataset.csv"),
        "name": "Vício em Celular (Adolescentes)",
        "description": "Dataset sobre dependência tecnológica",
        "icon": "📱",
        "loader": pd.read_csv
    }
}

def newdata():
    st.session_state.df = None
    st.session_state.outlier_check = False
    st.session_state.target = None
    st.session_state.split = None
    st.session_state.datetime = False
    st.session_state.normalization = False
    st.session_state.dummies = False

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
            .demo-card {
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                margin: 0.5rem 0;
                background-color: #f8f9fa;
            }
            .demo-card:hover {
                border-color: #ff6b6b;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def _handle_data_loading():
    """Gerencia todo o processo de carregamento de dados."""
    _handle_file_upload()
    _handle_demo_files()
    _display_loaded_data()

def _handle_file_upload():
    """Processa o upload de arquivos pelo usuário."""
    st.subheader("📤 Upload de Arquivo Personalizado")
    uploaded_file = st.file_uploader(
        "Escolha seu arquivo",
        type=["csv", "xlsx", "xls", "json", "feather", "parquet"],
        help="Formatos suportados: CSV, Excel (xlsx, xls), JSON, Feather, Parquet"
    )

    if uploaded_file:
        df = _load_uploaded_file(uploaded_file)
        if df is not None:
            newdata()
            st.session_state.df = df
            st.session_state.data_source = f"Upload: {uploaded_file.name}"
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

def _handle_demo_files():
    """Apresenta opções de arquivos de demonstração."""
    st.subheader("🎯 Datasets de Demonstração")
    st.markdown("Escolha um dos datasets pré-configurados para começar rapidamente:")
    
    # Criar colunas para os cards dos datasets
    cols = st.columns(len(DEMO_FILES))
    
    for i, (key, demo_info) in enumerate(DEMO_FILES.items()):
        with cols[i]:
            # Card personalizado para cada dataset
            st.markdown(f"""
                <div class="demo-card">
                    <div style="text-align: center; font-size: 2rem;">{demo_info['icon']}</div>
                    <div style="text-align: center; font-weight: bold; margin: 0.5rem 0;">
                        {demo_info['name']}
                    </div>
                    <div style="text-align: center; font-size: 0.9rem; color: #666;">
                        {demo_info['description']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                f"Carregar {demo_info['name']}", 
                key=f"demo_{key}",
                help=f"Carrega o dataset: {demo_info['description']}"
            ):
                _load_demo_file(key, demo_info)
                
def _load_demo_file(key: str, demo_info: dict):
    """Carrega um arquivo de demonstração específico."""
    try:
        demo_file = demo_info["path"]
        
        if not demo_file.exists():
            st.error(f"❌ Arquivo não encontrado: {demo_file}")
            st.info("💡 Certifique-se de que os arquivos estão na pasta correta:")
            st.code(f"📁 {demo_file}")
            return
        
        # Carregar o arquivo usando o loader apropriado
        df = demo_info["loader"](demo_file)
        
        # Resetar estado e carregar novos dados
        newdata()
        st.session_state.df = df
        st.session_state.data_source = f"Demo: {demo_info['name']}"
        
        st.success(f"✅ Dataset '{demo_info['name']}' carregado com sucesso!")
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar {demo_info['name']}: {str(e)}")
        st.info("🔍 Verifique se o arquivo existe e está no formato correto")

def _display_loaded_data():
    """Exibe os dados carregados se estiverem disponíveis."""
    if "df" in st.session_state and st.session_state.df is not None:
        st.subheader("📄 Visualização dos Dados Carregados")
        
        # Mostrar fonte dos dados
        if "data_source" in st.session_state:
            st.info(f"📊 Fonte atual: {st.session_state.data_source}")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        df = st.session_state.df
        
        with col1:
            st.metric("Total de Registros", f"{len(df):,}")
        with col2:
            st.metric("Total de Colunas", len(df.columns))
        with col3:
            # Contar valores nulos
            null_count = df.isnull().sum().sum()
            st.metric("Valores Nulos", f"{null_count:,}")
        with col4:
            # Tipos de dados únicos
            unique_types = df.dtypes.nunique()
            st.metric("Tipos de Dados", unique_types)
        
        # Preview dos dados
        st.markdown("**Preview dos Dados:**")
        st.dataframe(
            df.head(10),
            use_container_width=True,
            height=350
        )
        
        # Informações detalhadas em expander
        with st.expander("📋 Informações Detalhadas do Dataset"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Tipos de Dados por Coluna:**")
                type_info = pd.DataFrame({
                    'Coluna': df.columns,
                    'Tipo': df.dtypes.astype(str),
                    'Não-Nulos': df.count(),
                    'Nulos': df.isnull().sum()
                })
                st.dataframe(type_info, height=300)
            
            with col2:
                st.markdown("**Estatísticas Descritivas:**")
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    st.dataframe(df[numeric_cols].describe(), height=300)
                else:
                    st.info("Nenhuma coluna numérica encontrada")

# Função adicional para verificar disponibilidade dos arquivos
def check_demo_files_availability():
    """Verifica quais arquivos de demonstração estão disponíveis."""
    available_files = {}
    missing_files = {}
    
    for key, demo_info in DEMO_FILES.items():
        if demo_info["path"].exists():
            available_files[key] = demo_info
        else:
            missing_files[key] = demo_info
    
    return available_files, missing_files

# Função para criar a estrutura de pastas necessária
def create_data_structure():
    """Cria a estrutura de pastas necessária para os datasets."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    st.info(f"📁 Estrutura de pastas criada: {data_dir.absolute()}")
    
    # Listar arquivos esperados
    st.markdown("**Arquivos esperados:**")
    for demo_info in DEMO_FILES.values():
        status = "✅" if demo_info["path"].exists() else "❌"
        st.markdown(f"{status} `{demo_info['path']}`")