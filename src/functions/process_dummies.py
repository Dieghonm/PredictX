import streamlit as st
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

def criar_dummies_dataframe(df):
    """
    Função para criar variáveis dummy (one-hot encoding) com interface Streamlit.
    Inclui botão de explicação, seleção de colunas e controles de desfazer/gravar.
    
    Args:
        df (pd.DataFrame): DataFrame a ser processado
        
    Returns:
        pd.DataFrame: DataFrame com as variáveis dummy ou original se o usuário cancelar
    """
    # Inicializa o estado da sessão se não existir
    if 'df_original_dummies' not in st.session_state:
        st.session_state.df_original_dummies = df.copy()
    
    # Botão de explicação
    with st.expander("ℹ️ Como funcionam as variáveis dummy?"):
        st.markdown("""
        **Variáveis dummy (one-hot encoding)** transformam categorias em colunas binárias:
        
        - Cada categoria vira uma nova coluna com valores 0 ou 1
        - Exemplo: "cor" com valores ["vermelho", "azul"] vira:
          - cor_vermelho: 1 quando for vermelho, 0 caso contrário
          - cor_azul: 1 quando for azul, 0 caso contrário
        
        **Quando usar?**
        - Para categorias sem ordem natural (nominais)
        - Quando o número de categorias é pequeno (ideal <10)
        
        **Cuidados:**
        - Pode aumentar muito o número de colunas (problema da dimensionalidade)
        - Em colunas com muitas categorias, prefira Target Encoding
        """)
    
    # Selecionar colunas categóricas
    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not colunas_categoricas:
        st.warning("Nenhuma coluna categórica encontrada para criar dummies!")
        return df
    
    # Selecionar colunas para transformar
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas para criar variáveis dummy:",
        options=colunas_categoricas,
        default=colunas_categoricas
    )
    
    # Opções avançadas
    with st.expander("⚙️ Opções avançadas"):
        drop_first = st.checkbox(
            "Remover primeira categoria (evitar multicolinearidade)",
            help="Útil para modelos de regressão linear"
        )
        
        handle_unknown = st.selectbox(
            "Como lidar com novas categorias?",
            options=['error', 'ignore', 'create'],
            help="O que fazer se aparecerem categorias não vistas durante o treino"
        )
    
    # Aplicar transformação
    if st.button("Criar Variáveis Dummy"):
        try:
            df_dummies = df.copy()
            
            # Verificar cardinalidade
            high_cardinality = []
            for col in colunas_selecionadas:
                if df[col].nunique() > 15:
                    high_cardinality.append(col)
            
            if high_cardinality:
                st.warning(f"Cuidado! Colunas com alta cardinalidade: {', '.join(high_cardinality)}. Considere usar Target Encoding.")
            
            # Criar dummies
            df_dummies = pd.get_dummies(
                df_dummies,
                columns=colunas_selecionadas,
                drop_first=drop_first,
                dummy_na=False
            )
            
            st.success("Variáveis dummy criadas com sucesso!")
            st.dataframe(df_dummies.head())
            
            # Botões de controle
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏪ Desfazer Transformação"):
                    df_dummies = st.session_state.df_original_dummies.copy()
                    st.session_state.df = st.session_state.df_original_dummies.copy()
                    st.rerun()
            
            with col2:
                if st.button("💾 Gravar Alterações"):
                    st.session_state.df = df_dummies.copy()
                    st.success("DataFrame com dummies gravado com sucesso!")
                    st.session_state.dummies_applied = True
                    st.rerun()
            
            return df_dummies
            
        except Exception as e:
            st.error(f"Erro ao criar dummies: {str(e)}")
            return df
    
    return df