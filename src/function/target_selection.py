import streamlit as st
import pandas as pd

def select_target(df, colunas):
    with st.expander("🔍 **Seleção da Variável Alvo (Target)**", expanded=True):
        st.markdown(
            "Selecione a coluna que contém o valor que seu modelo deve prever. "
            "Esta será a variável dependente na análise."
        )

        target_col = st.selectbox(
            "Variável alvo:",
            options=colunas,
            index=len(colunas) - 1,
            key="target_selectbox",
            help="Esta coluna será usada como o valor a ser previsto pelo modelo."
        )

        st.code(f"Valores únicos na coluna '{target_col}':\n{df[target_col].unique()[:10]}", language='python')
        
        if len(df[target_col].unique()) > 10:
            st.warning("⚠️ Esta coluna tem muitos valores únicos. Verifique se é realmente uma variável alvo adequada.")
        
        
        if st.button(f"Selecionar {target_col} como alvo "):
            st.session_state.target = target_col
            st.rerun()
        


    return target_col