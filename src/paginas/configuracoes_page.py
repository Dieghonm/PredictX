import streamlit as st
import pandas as pd
from functions.data_handling import check_data_loaded, get_missing_data_stats, get_numeric_columns
from functions.missing_values import handle_missing_values
from functions.outliers_handling import handle_outliers
from functions.target_selection import select_target
from functions.data_splitting import data_splitting_options
from functions.config_saving import save_config
from functions.duplicates_handling import check_duplicates

def mostrar():
    st.title("⚙️ Configurações do Modelo")
    
    # Verificar se os dados foram carregados
    check_data_loaded()
    
    # Obter dados e estatísticas
    df = st.session_state.df.copy()
    colunas = df.columns.tolist()
    faltantes_df = get_missing_data_stats(df)
    numeric_cols = get_numeric_columns(df)
    
    # Tratar valores faltantes
    if not faltantes_df.empty:
        df = handle_missing_values(df, faltantes_df)

    df = check_duplicates(df)
    
    # Lidar com outliers (apenas para colunas numéricas)
    if numeric_cols:
        df = handle_outliers(df, numeric_cols)
    
    # Seleção da variável alvo
    target_col = select_target(df, colunas)
    
    # Opções de divisão dos dados
    split_config = data_splitting_options(df, colunas)
    
    # Configurações avançadas
    with st.expander("⚡ Configurações Avançadas"):
        random_state = st.number_input(
            "Random State", 
            min_value=0, value=42,
            help="Semente aleatória para reprodutibilidade"
        )
        shuffle = st.checkbox(
            "Embaralhar dados", 
            value=True,
            help="Se os dados devem ser embaralhados antes da divisão"
        )
    
    # Salvar configurações
    if st.button("💾 Salvar Todas as Configurações", type="primary"):
        metodo_divisao = "Por porcentagem" if split_config["method"] == "percentage" else "Por coluna específica"
        save_config(target_col, metodo_divisao, split_config, random_state, shuffle)