import pandas as pd
import streamlit as st

def check_data_loaded():
    if "df" not in st.session_state or st.session_state.df.empty:
        st.warning("⚠️ Nenhum dado carregado. Vá para a aba **'Data'**.")
        st.stop()

def get_missing_data_stats(df):
    total_linhas = len(df)
    dados_faltantes = df.isna().sum()
    dados_faltantes_pct = (dados_faltantes / total_linhas * 100).round(2)
    
    faltantes_df = pd.DataFrame({
        "Coluna": dados_faltantes.index,
        "Qtd. Faltantes": dados_faltantes.values,
        "% Faltantes": dados_faltantes_pct.values
    }).sort_values(by="% Faltantes", ascending=False)
    
    return faltantes_df[faltantes_df["Qtd. Faltantes"] > 0]

def get_numeric_columns(df):
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()