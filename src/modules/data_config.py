import streamlit as st
import pandas as pd

from functions import (
    process_duplicates,
    process_missing,
    process_outliers,
    target_selection,
    data_splitting
)

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
    st.title("⚙️ Configurações do Modelo")
    _setup_page_config()
    
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        colunas = df.columns.tolist()
        numeric_cols = process_outliers.get_numeric_columns(df)


        if df.isnull().any().any():
            faltantes_df = process_missing.get_missing_data_stats(df)
            df = process_missing.handle_missing_values(df, faltantes_df)

        elif df.duplicated().any():
            df = process_duplicates.check_duplicates(df)
        
        elif not st.session_state.outlier_check:
            df = process_outliers.handle_outliers(df, numeric_cols)

        elif not st.session_state.target :
            target_selection.select_target(df, colunas)

        elif not st.session_state.split:
            data_splitting.data_splitting_options(df, colunas)
   
        else:
            st.info(f"else")
   

    else:
        st.warning("⚠️ Carregue os dados na aba **Data**.")

    st.info(f"**Teste** `{st.session_state.target, st.session_state.split}`")
                    


