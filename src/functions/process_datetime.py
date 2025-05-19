import pandas as pd
import streamlit as st

def get_date_columns(df):
    """Identifica colunas que podem ser convertidas para datetime."""
    date_cols = []
    for col in df.columns:
        # Tenta converter para datetime
        try:
            if pd.to_datetime(df[col], errors='coerce').notna().any():
                date_cols.append(col)
        except:
            continue
    return date_cols

def datetime_options(df):
    """Interface para seleção e processamento de colunas de data."""
    with st.expander("🔍 ** Formatar data **", expanded=True):
        date_columns = get_date_columns(df)
        
        if not date_columns:
            st.info("Nenhuma coluna com formato de data identificada.")
            return df
    
        selected_dates = st.multiselect(
            "Selecione colunas para converter para datetime:",
            options=date_columns,
            default=[]
        )
        
        # Botão para executar a conversão
        if st.button("Converter colunas selecionadas"):
            if selected_dates:
                for col in selected_dates:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
                    st.session_state.df = df
                st.success(f"Colunas convertidas para datetime: {selected_dates}")
                st.rerun()

            else:
                st.warning("Nenhuma coluna selecionada para conversão.")
        if st.session_state.df is not None:
            st.dataframe(df.head(5))
        if st.button("Proxima etapa"):
            st.session_state.datetime = True
                
    return df