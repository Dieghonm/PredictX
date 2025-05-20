import pandas as pd
import streamlit as st

def get_date_columns(df, sample_size=500, threshold=0.7):
    date_cols = []
    
    sample_df = df.sample(min(sample_size, len(df))) if len(df) > sample_size else df
    
    for col in sample_df.columns:
        if pd.api.types.is_numeric_dtype(sample_df[col]) and not any(name in col.lower() for name in ['date', 'time', 'year']):
            continue
            
        try:
            converted = pd.to_datetime(sample_df[col], errors='coerce', infer_datetime_format=True)
            success_rate = converted.notna().mean()
            
            if success_rate >= threshold:
                date_cols.append(col)
        except (TypeError, ValueError):
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
            default=[date_columns[0]]
        )
        
        if st.button("Converter colunas selecionadas"):
            if selected_dates:
                for col in selected_dates:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')
                    st.session_state.df = df
                st.success(f"Colunas convertidas para datetime (dd/mm/aaaa): {selected_dates}")
                st.rerun()
            else:
                st.warning("Nenhuma coluna selecionada para conversão.")
                
        if st.session_state.df is not None:
            st.dataframe(df.head(5))
            
        if st.button("Próxima etapa"):
            st.session_state.datetime = True
            st.rerun()
                
    return df