import streamlit as st
import pandas as pd

from functions import (
    process_duplicates,
    process_missing,
    process_outliers,
    process_datetime,
    process_normalization,
    process_dummies,
    target_selection,
    data_splitting,
    config_buttons,
    show_preprocessing
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
        
        elif not st.session_state.datetime:
            df = process_datetime.datetime_options(df)
            st.session_state.datetime_processed = True
            st.session_state.df = df 

        elif not st.session_state.normalization:
            process_normalization.normalizar_dataframe(df)
            
        elif False:
            st.info(f"scaling...")
            
        elif False:
            st.info(f"encoding")
            
        elif False:
            st.info(f"else")
            
        elif False:
            st.info(f"else")

        elif not st.session_state.target :
            target_selection.select_target(df, colunas)

        elif not st.session_state.dummies:
            process_dummies.criar_dummies_dataframe(df)
            
        elif not st.session_state.split:
            data_splitting.data_splitting_options(df, colunas)
   
        else:
            show_preprocessing.show_preprocessing_results()
        config_buttons.config_buttons()

    else:
        st.warning("⚠️ Carregue os dados na aba **Data**.")