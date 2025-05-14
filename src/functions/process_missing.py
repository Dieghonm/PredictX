import pandas as pd
import streamlit as st

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

def handle_missing_values(df, faltantes_df):
    with st.expander("❗ **Tratamento de variável missing**", expanded=True):
        st.warning(f"⚠️ **{len(faltantes_df)} colunas com dados faltantes**")
        st.dataframe(faltantes_df)

        if st.checkbox("Remover linhas com dados faltantes", key="remove_missing"):
            df = df.dropna()
            st.session_state.df = df
            st.rerun()

        coluna_preencher = st.selectbox(
            "Coluna para preencher missing:",
            faltantes_df["Coluna"].tolist(),
            key="coluna_preencher"
        )

        metodo = st.radio(
            "Método de preenchimento:",
            ["Zero", "Média", "Mediana", "Moda", "Valor Personalizado"],
            key="metodo_preenchimento"
        )

        valor_personalizado = None
        if metodo == "Valor Personalizado":
            valor_personalizado = st.text_input("Digite o valor personalizado", key="valor_custom")

        aplicar = st.button("Aplicar Preenchimento", key="botao_aplicar")

        if aplicar:
            if metodo == "Zero":
                df[coluna_preencher] = df[coluna_preencher].fillna(0)
            elif metodo == "Média":
                df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].mean())
            elif metodo == "Mediana":
                df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].median())
            elif metodo == "Moda":
                df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].mode()[0])
            elif metodo == "Valor Personalizado" and valor_personalizado:
                df[coluna_preencher] = df[coluna_preencher].fillna(valor_personalizado)

            st.session_state.df = df
            st.rerun()
    
    return df