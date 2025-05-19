import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def normalizar_dataframe(df):
    """
    Função para normalizar um DataFrame com interface Streamlit.
    Inclui botão de explicação e opções de normalização.
    
    Args:
        df (pd.DataFrame): DataFrame a ser normalizado
        
    Returns:
        pd.DataFrame: DataFrame normalizado ou original se o usuário cancelar
    """
    
    # Botão de explicação
    with st.expander("ℹ️ Como funciona a normalização?"):
        st.markdown("""
        **Normalização de dados** transforma suas colunas numéricas para uma escala comum:
        
        - **MinMax (0-1):** Escala os valores para ficarem entre 0 e 1
        - **Padronização (Z-score):** Transforma para média 0 e desvio padrão 1
        - **Logarítmica:** Aplica log natural para dados com distribuição exponencial
        
        Por que normalizar?
        - Algoritmos de ML performam melhor com dados na mesma escala
        - Facilita comparação entre variáveis
        - Reduz influência de outliers
        """)
        
    # Selecionar tipo de normalização
    metodo = st.radio(
        "Selecione o método de normalização:",
        options=[
            "MinMax (0-1)",
            "Padronização (Z-score)",
            "Logarítmica",
            "Personalizar colunas"
        ]
    )
    
    # Selecionar colunas para normalizar
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    
    if metodo == "Personalizar colunas":
        colunas_selecionadas = st.multiselect(
            "Selecione as colunas para normalizar:",
            options=colunas_numericas,
            default=colunas_numericas
        )
    else:
        colunas_selecionadas = colunas_numericas
    
    # Aplicar normalização
    if st.button("Aplicar Normalização"):
        df_normalizado = df.copy()
        
        try:
            if metodo == "MinMax (0-1)":
                scaler = MinMaxScaler()
                df_normalizado[colunas_selecionadas] = scaler.fit_transform(df[colunas_selecionadas])
                
            elif metodo == "Padronização (Z-score)":
                scaler = StandardScaler()
                df_normalizado[colunas_selecionadas] = scaler.fit_transform(df[colunas_selecionadas])
                
            elif metodo == "Logarítmica":
                for col in colunas_selecionadas:
                    if (df[col] > 0).all():  # Só aplica log se todos valores forem positivos
                        df_normalizado[col] = np.log(df[col])
                    else:
                        st.warning(f"Não foi possível aplicar log na coluna {col} (contém valores <= 0)")
            
            st.success("Normalização aplicada com sucesso!")
            st.dataframe(df_normalizado.head(5))
            col1, col2 = st.columns(2)

            # Botões de controle
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏪ Desfazer Normalização"):
                    df_normalizado = st.session_state.df_original.copy()
                    st.session_state.df = st.session_state.df_original.copy()
                    st.rerun()
            
            with col2:
                if st.button("💾 Gravar Alterações"):
                    st.session_state.df = df_normalizado.copy()
                    st.success("Alterações gravadas com sucesso!")
                    st.session_state.normalization = True
                    st.rerun()

        except Exception as e:
            st.error(f"Erro ao normalizar: {str(e)}")
            return df
    if st.button("✅ Finalizar normalização"):
        st.session_state.normalization = True
        st.rerun()
    
    return df
