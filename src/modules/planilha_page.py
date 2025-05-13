import streamlit as st
import pandas as pd

def mostrar():
    st.title("📊 Visualização da Planilha")
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head(100))



        df = st.session_state.df
        colunas = df.columns.tolist()
        total_linhas = len(df)
        dados_faltantes = df.isna().sum()
        dados_faltantes_pct = (dados_faltantes / total_linhas * 100).round(2)
        faltantes_df = pd.DataFrame({
            "Coluna": dados_faltantes.index,
            "Qtd. Faltantes": dados_faltantes.values,
            "% Faltantes": dados_faltantes_pct.values
        }).sort_values(by="% Faltantes", ascending=False)
        faltantes_df = faltantes_df[faltantes_df["Qtd. Faltantes"] > 0]

        st.warning(f"⚠️ **Dados faltantes detectados** ({len(faltantes_df)} colunas afetadas)")

        faltantes_df = pd.DataFrame({
            "Coluna": dados_faltantes.index,
            "Qtd. Faltantes": dados_faltantes.values,
            "% Faltantes": dados_faltantes_pct.values
        })
        st.dataframe(faltantes_df[faltantes_df["Qtd. Faltantes"] > 0])




    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para a aba **Data**.")