import streamlit as st
from functions.outliers_utils import detectar_outliers, plot_outliers

def handle_outliers(df, numeric_cols):
    if 'hide_numeric' not in st.session_state:
        st.session_state.hide_numeric = False

    if not st.session_state.hide_numeric:
        with st.expander("📊 Detecção de Outliers", expanded=True):
            st.header("Identificação de Outliers")

            coluna_analise = st.selectbox(
                "Selecione a coluna para análise:",
                numeric_cols,
                key="coluna_outlier"
            )
            
            if st.button("🔍 Verificar Outliers", help="Clique para identificar outliers na coluna selecionada"):
                lim_inf, lim_sup, outliers = detectar_outliers(df, coluna_analise)
                
                st.write(f"**Limites para {coluna_analise}:**")
                st.write(f"- Limite inferior: {lim_inf:.4f}")
                st.write(f"- Limite superior: {lim_sup:.4f}")
                st.write(f"- Número de outliers encontrados: {len(outliers)}")

                freq_outliers = (
                    outliers[coluna_analise]
                    .value_counts()
                    .to_frame('Ocorrências')
                    .query('Ocorrências < 5')
                )

                if not freq_outliers.empty:
                    menor_valor_corte = freq_outliers.index.min()
                    st.success(f"⏬ Limiar automático definido em: {menor_valor_corte:.4f}")
                    
                    outliers_filtrados = outliers[outliers[coluna_analise] >= menor_valor_corte]
                    
                    st.write("📈 Distribuição dos outliers significativos:")
                    st.dataframe(
                        outliers_filtrados[coluna_analise]
                        .value_counts()
                        .to_frame('Ocorrências')
                        .sort_values(coluna_analise)
                    )
                    
                    st.pyplot(plot_outliers(outliers_filtrados, coluna_analise))
                    
                    if st.button("✂️ Cortar Outliers"):
                        df = df[df[coluna_analise] < menor_valor_corte]
                        st.session_state.df = df
                        st.success("Dados atualizados com remoção de outliers!")
                        st.rerun()
                else:
                    st.warning("Não foram encontrados outliers raros (com menos de 5 ocorrências)")

        if st.button("❌ Pular análise de outliers"):
            st.session_state.hide_numeric = True
            st.rerun()
    
    return df