import streamlit as st
import pandas as pd
from functions.outliers_utils import detectar_outliers, verificar_outliers, plot_outliers

def mostrar():
    st.title("📈 Gráficos (em breve)")
    if st.session_state.df is not None:
        st.write("Você poderá criar gráficos com os dados aqui.")
        st.title("⚙️ Configurações do Modelo")
        df = st.session_state.df.copy()
        
        with st.expander("📊 Detecção de Outliers", expanded=True):
            st.header("Identificação de Outliers")
            
            # Selecionar coluna para análise
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            coluna_analise = st.selectbox(
                "Selecione a coluna para análise:",
                numeric_cols,
                key="coluna_outlier"
            )
            
            if st.button("Verificar Outliers"):
                lim_inf, lim_sup, outliers = detectar_outliers(df, coluna_analise)
                
                st.write(f"**Limites para {coluna_analise}:**")
                st.write(f"- Limite inferior: {lim_inf:.4f}")
                st.write(f"- Limite superior: {lim_sup:.4f}")
                st.write(f"- Número de outliers encontrados: {len(outliers)}")
                
                if len(outliers) > 0:
                    st.write("**Amostra de outliers:**")
                    st.dataframe(outliers[[coluna_analise]].sort_values(coluna_analise))
                    
                    # Mostrar gráficos
                    st.pyplot(plot_outliers(df, coluna_analise))


    else:
        st.warning("⚠️ Carregue os dados na aba **Data**.")