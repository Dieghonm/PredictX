import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
from datetime import datetime
import io
import plotly.express as px
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================================

st.set_page_config(
    page_title="Sistema de Escoragem de Crédito",
    page_icon="💳",
    layout="wide"
)

# ============================================================================
# CLASSES E FUNÇÕES AUXILIARES
# ============================================================================

class OutlierRemover(BaseEstimator, TransformerMixin):
    """Remove outliers usando IQR ou Z-score"""
    def __init__(self, method='iqr', factor=1.5):
        self.method = method
        self.factor = factor
        self.bounds_ = {}
    
    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.method == 'iqr':
                    Q1 = X[col].quantile(0.25)
                    Q3 = X[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - self.factor * IQR
                    upper_bound = Q3 + self.factor * IQR
                    self.bounds_[col] = (lower_bound, upper_bound)
        return self
    
    def transform(self, X):
        X_transformed = X.copy()
        if isinstance(X_transformed, pd.DataFrame):
            for col, (lower, upper) in self.bounds_.items():
                if col in X_transformed.columns:
                    median_val = X_transformed[col].median()
                    X_transformed.loc[X_transformed[col] < lower, col] = median_val
                    X_transformed.loc[X_transformed[col] > upper, col] = median_val
        return X_transformed

@st.cache_data
def load_model(model_path):
    """Carrega o modelo treinado"""
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model, True
    except Exception as e:
        return str(e), False

def diagnose_model(model):
    """Analisa o modelo para descobrir o formato esperado dos dados"""
    diagnosis = {}
    
    try:
        preprocessor = model.named_steps['preprocessor']
        
        if hasattr(preprocessor, 'transformers_'):
            for name, transformer, columns in preprocessor.transformers_:
                if name == 'cat':
                    onehot_encoder = transformer.named_steps['onehot']
                    if hasattr(onehot_encoder, 'categories_'):
                        diagnosis['categorical_columns'] = columns
                        diagnosis['categories_per_column'] = {}
                        for i, col in enumerate(columns):
                            diagnosis['categories_per_column'][col] = list(onehot_encoder.categories_[i])
                
                elif name == 'num':
                    diagnosis['numerical_columns'] = columns
        
        diagnosis['success'] = True
        
    except Exception as e:
        diagnosis['success'] = False
        diagnosis['error'] = str(e)
    
    return diagnosis

def preprocess_data(df, model_diagnosis=None):
    """Aplica pré-processamento nos dados baseado no diagnóstico do modelo"""
    df_processed = df.copy()
    
    # Limpeza básica
    if 'id_cliente' in df_processed.columns:
        df_processed.drop(columns=['id_cliente'], inplace=True)
    
    # Converter datas se existir
    if 'data_ref' in df_processed.columns:
        try:
            df_processed['data_ref'] = pd.to_datetime(df_processed['data_ref'])
        except:
            st.warning("Não foi possível converter a coluna 'data_ref'")
    
    # Padronizar colunas boolean
    for col in ['posse_de_veiculo', 'posse_de_imovel']:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].replace({
                'False': 'N', 'True': 'S', False: 'N', True: 'S'
            })
    
    # Padronizar educação
    mapeamento_educacao = {
        'Secundário': 'Médio',
        'Primário': 'Fundamental',
    }
    if 'educacao' in df_processed.columns:
        df_processed['educacao'] = df_processed['educacao'].replace(mapeamento_educacao)
    
    # Processar com base no diagnóstico do modelo
    if model_diagnosis and model_diagnosis.get('success'):
        categories_expected = model_diagnosis.get('categories_per_column', {})
        
        for col, expected_categories in categories_expected.items():
            if col in df_processed.columns:
                if any(val in expected_categories for val in [True, False]):
                    # Modelo espera booleanos
                    mapping = {
                        'Y': True, 'N': False, 'S': True,
                        'YES': True, 'NO': False, 'SIM': True, 'NAO': False, 'NÃO': False,
                        '1': True, '0': False, 1: True, 0: False,
                        'TRUE': True, 'FALSE': False, 'T': True, 'F': False,
                        True: True, False: False
                    }
                    df_processed[col] = df_processed[col].astype(str).str.upper().map(mapping)
                    df_processed[col] = df_processed[col].fillna(False)
                else:
                    # Modelo espera strings
                    df_processed[col] = df_processed[col].astype(str)
                    df_processed[col] = df_processed[col].replace(['nan', 'None'], 'missing')
                    df_processed[col] = df_processed[col].fillna('missing')
    
    # Processar colunas numéricas
    colunas_numericas = ['qtd_filhos', 'idade', 'tempo_emprego', 'qt_pessoas_residencia', 'renda']
    for col in colunas_numericas:
        if col in df_processed.columns:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            df_processed[col] = df_processed[col].fillna(0)
    
    # Determinar colunas disponíveis
    if model_diagnosis and 'categorical_columns' in model_diagnosis:
        colunas_categoricas = model_diagnosis['categorical_columns']
        colunas_numericas = model_diagnosis['numerical_columns']
    else:
        colunas_categoricas = ['sexo', 'posse_de_veiculo', 'posse_de_imovel', 
                              'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia']
        colunas_numericas = ['qtd_filhos', 'idade', 'tempo_emprego', 
                            'qt_pessoas_residencia', 'renda']
    
    colunas_existentes = list(colunas_categoricas) + list(colunas_numericas)
    colunas_disponiveis = [col for col in colunas_existentes if col in df_processed.columns]
    
    return df_processed, colunas_disponiveis

def generate_score_report(df_original, predictions, probabilities):
    """Gera relatório de escoragem"""
    df_resultado = df_original.copy()
    df_resultado['score_probabilidade'] = probabilities
    df_resultado['score_classe'] = predictions
    df_resultado['score_rating'] = pd.cut(
        probabilities,
        bins=[0, 0.1, 0.3, 0.5, 0.7, 1.0],
        labels=['Excelente', 'Bom', 'Regular', 'Ruim', 'Péssimo']
    )
    
    return df_resultado

# ============================================================================
# TELAS DA APLICAÇÃO
# ============================================================================

def tela_carregamento():
    """Tela para carregar modelo e dados"""
    st.title("📁 Carregamento de Dados e Modelo")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Carregamento do Modelo
    with col1:
        st.header("🤖 Carregamento do Modelo")
        
        model_file = st.text_input("Nome do arquivo do modelo:", value="model_final.pkl")
        
        if st.button("🔄 Carregar Modelo", type="primary"):
            with st.spinner("Carregando modelo..."):
                model_result, model_success = load_model(model_file)
                
                if model_success:
                    st.session_state.model = model_result
                    st.success("✅ Modelo carregado com sucesso!")
                    
                    # Diagnosticar o modelo
                    diagnosis = diagnose_model(model_result)
                    st.session_state.model_diagnosis = diagnosis
                    
                    if diagnosis['success']:
                        st.info("🔍 Diagnóstico do modelo realizado!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Diagnóstico falhou: {diagnosis.get('error', 'Erro desconhecido')}")
                else:
                    st.error(f"❌ Erro ao carregar modelo: {model_result}")
    
    # Carregamento dos Dados
    with col2:
        st.header("📊 Carregamento dos Dados")
        
        uploaded_file = st.file_uploader(
            "Selecione o arquivo CSV:",
            type=['csv'],
            help="Faça upload de um arquivo CSV com os dados para escoragem"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df_original = df
                st.success(f"✅ Arquivo carregado: {len(df)} registros")
                
                # Métricas
                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.metric("Registros", len(df))
                with col_info2:
                    st.metric("Colunas", len(df.columns))
                with col_info3:
                    st.metric("Valores Nulos", df.isnull().sum().sum())
                
                # Prévia
                with st.expander("👀 Prévia dos Dados"):
                    st.dataframe(df.head(10))
                
            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
    
    # Status Geral
    st.markdown("---")
    st.header("📋 Status Geral")
    
    col_status1, col_status2 = st.columns(2)
    
    with col_status1:
        if 'model' in st.session_state:
            st.success("🤖 Modelo: Carregado")
        else:
            st.error("🤖 Modelo: Não carregado")
    
    with col_status2:
        if 'df_original' in st.session_state:
            st.success("📊 Dados: Carregados")
        else:
            st.error("📊 Dados: Não carregados")
    
    if 'model' in st.session_state and 'df_original' in st.session_state:
        st.success("🎉 Tudo pronto! Vá para a aba 'Diagnóstico' para continuar.")

def tela_diagnostico():
    """Tela para diagnóstico e validação dos dados"""
    st.title("🔍 Diagnóstico e Validação")
    st.markdown("---")
    
    if 'df_original' not in st.session_state:
        st.error("❌ Dados não carregados. Vá para a aba 'Carregamento' primeiro.")
        return
    
    df = st.session_state.df_original
    
    col1, col2 = st.columns(2)
    
    # Análise dos Dados
    with col1:
        st.header("📊 Análise dos Dados")
        
        # Informações gerais
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Registros", len(df))
        with col_info2:
            st.metric("Colunas", len(df.columns))
        with col_info3:
            st.metric("Valores Nulos", df.isnull().sum().sum())
        
        # Colunas disponíveis
        st.subheader("📋 Colunas Disponíveis")
        for col in df.columns:
            st.write(f"• {col} ({df[col].dtype})")
    
    # Diagnóstico do Modelo
    with col2:
        st.header("🤖 Diagnóstico do Modelo")
        
        if 'model_diagnosis' in st.session_state and st.session_state.model_diagnosis['success']:
            diagnosis = st.session_state.model_diagnosis
            
            st.subheader("📋 Colunas Categóricas")
            if 'categorical_columns' in diagnosis:
                for col in diagnosis['categorical_columns']:
                    st.write(f"• {col}")
            
            st.subheader("🔢 Colunas Numéricas")
            if 'numerical_columns' in diagnosis:
                for col in diagnosis['numerical_columns']:
                    st.write(f"• {col}")
        else:
            st.error("❌ Diagnóstico do modelo não disponível")
    
    st.markdown("---")
    st.dataframe(df.head())
    
    # Análise de Valores Únicos
    st.subheader("🔍 Análise de Categorias")
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        with st.expander(f"📝 {col}"):
            unique_vals = df[col].unique()
            st.write(f"**Valores únicos ({len(unique_vals)}):** {list(unique_vals)}")
            
            if len(unique_vals) > 20:
                st.warning("⚠️ Muitas categorias únicas - pode precisar de agrupamento")

def tela_escoragem():
    """Tela principal de escoragem"""
    st.title("🚀 Escoragem e Resultados")
    st.markdown("---")
    
    # Verificações iniciais
    if 'model' not in st.session_state:
        st.error("❌ Modelo não carregado. Vá para a aba 'Carregamento' primeiro.")
        return
    
    if 'df_original' not in st.session_state:
        st.error("❌ Dados não carregados. Vá para a aba 'Carregamento' primeiro.")
        return
    
    # Execução da Escoragem
    st.header("⚡ Executar Escoragem")
    
    col_exec1, col_exec2 = st.columns([2, 1])
    
    with col_exec1:
        if st.button("🚀 Executar Escoragem", type="primary", use_container_width=True):
            with st.spinner("Executando escoragem..."):
                try:
                    start_time = time.time()
                    
                    df = st.session_state.df_original
                    model_diagnosis = st.session_state.get('model_diagnosis', None)
                    
                    # Pré-processamento
                    df_processed, colunas_disponiveis = preprocess_data(df, model_diagnosis)
                    
                    # Preparar dados para o modelo
                    X_score = df_processed[colunas_disponiveis]
                    
                    # Fazer predições
                    predictions = st.session_state.model.predict(X_score)
                    probabilities = st.session_state.model.predict_proba(X_score)[:, 1]
                    
                    end_time = time.time()
                    
                    # Gerar relatório
                    df_resultado = generate_score_report(df, predictions, probabilities)
                    
                    # Armazenar resultados
                    st.session_state.df_resultado = df_resultado
                    st.session_state.processing_time = end_time - start_time
                    
                    st.success(f"✅ Escoragem concluída em {end_time - start_time:.2f} segundos!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Erro durante a escoragem: {str(e)}")
                    st.error("🛠️ Verifique se os dados estão no formato correto")
    
    with col_exec2:
        if 'df_resultado' in st.session_state:
            st.success("✅ Escoragem Concluída")
            st.metric("Tempo", f"{st.session_state.processing_time:.2f}s")
        else:
            st.info("⏳ Aguardando execução")
    
    # Resultados
    if 'df_resultado' in st.session_state:
        mostrar_resultados()

def mostrar_resultados():
    """Mostra os resultados da escoragem"""
    st.markdown("---")
    st.header("📊 Resumo dos Resultados")
    
    df_res = st.session_state.df_resultado
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_prob = df_res['score_probabilidade'].mean()
        st.metric("Probabilidade Média", f"{avg_prob:.1%}")
    
    with col2:
        high_risk = (df_res['score_probabilidade'] > 0.5).sum()
        st.metric("Alto Risco", f"{high_risk} ({high_risk/len(df_res):.1%})")
    
    with col3:
        low_risk = (df_res['score_probabilidade'] <= 0.5).sum()
        st.metric("Baixo Risco", f"{low_risk} ({low_risk/len(df_res):.1%})")
    
    with col4:
        st.metric("Total", len(df_res))
    
    # Gráficos
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Distribuição de Probabilidades")
        fig_hist = px.histogram(
            df_res, 
            x='score_probabilidade',
            nbins=20,
            title="Distribuição de Probabilidades"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_chart2:
        st.subheader("🎯 Distribuição por Rating")
        rating_counts = df_res['score_rating'].value_counts()
        fig_bar = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            title="Quantidade por Rating"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabela de resultados
    st.markdown("---")
    st.header("📋 Resultados Detalhados")
    
    # Filtros
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        rating_filter = st.multiselect(
            "Filtrar por Rating:",
            options=df_res['score_rating'].unique(),
            default=df_res['score_rating'].unique()
        )
    
    with col_filter2:
        prob_range = st.slider(
            "Filtrar por Probabilidade:",
            min_value=0.0,
            max_value=1.0,
            value=(0.0, 1.0),
            step=0.01
        )
    
    # Aplicar filtros
    df_filtered = df_res[
        (df_res['score_rating'].isin(rating_filter)) &
        (df_res['score_probabilidade'] >= prob_range[0]) &
        (df_res['score_probabilidade'] <= prob_range[1])
    ]
    
    st.dataframe(df_filtered, use_container_width=True, height=400)
    st.caption(f"Mostrando {len(df_filtered)} de {len(df_res)} registros")
    
    # Download
    st.markdown("---")
    st.header("💾 Download dos Resultados")
    
    csv_buffer = io.StringIO()
    df_res.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="📥 Baixar Resultados (CSV)",
        data=csv_data,
        file_name=f"escoragem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================================================
# SIDEBAR E NAVEGAÇÃO
# ============================================================================

def criar_sidebar():
    """Cria a barra lateral com navegação e status"""
    st.sidebar.title("🧭 Navegação")
    st.sidebar.markdown("---")
    
    # Seleção da tela
    tela_selecionada = st.sidebar.radio(
        "Selecione a tela:",
        ["📁 Carregamento", "🔍 Diagnóstico", "🚀 Escoragem"],
        index=0
    )
    
    # Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Status")
    
    if 'model' in st.session_state:
        st.sidebar.success("🤖 Modelo: Carregado")
    else:
        st.sidebar.error("🤖 Modelo: Não carregado")
    
    if 'df_original' in st.session_state:
        st.sidebar.success("📊 Dados: Carregados")
        st.sidebar.info(f"📈 {len(st.session_state.df_original)} registros")
    else:
        st.sidebar.error("📊 Dados: Não carregados")
    
    if 'df_resultado' in st.session_state:
        st.sidebar.success("✅ Escoragem: Concluída")
    else:
        st.sidebar.warning("⏳ Escoragem: Pendente")
    
    st.sidebar.markdown("---")
    
    # Botão limpar cache
    if st.sidebar.button("🗑️ Limpar Cache", use_container_width=True):
        st.cache_data.clear()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.sidebar.success("Cache limpo!")
        st.rerun()
    
    return tela_selecionada

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação"""
    
    # Criar sidebar e obter tela selecionada
    tela_selecionada = criar_sidebar()
    
    # Roteamento das telas
    if tela_selecionada == "📁 Carregamento":
        tela_carregamento()
    elif tela_selecionada == "🔍 Diagnóstico":
        tela_diagnostico()
    elif tela_selecionada == "🚀 Escoragem":
        tela_escoragem()

if __name__ == "__main__":
    main()