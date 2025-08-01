import streamlit as st
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

def criar_dummies_dataframe(df):
    """
    Função para criar variáveis dummy (one-hot encoding) com interface Streamlit.
    Mostra os 5 primeiros registros após gravar/desfazer.
    """
    # Inicializa estados da sessão
    if 'df_original_dummies' not in st.session_state:
        st.session_state.df_original_dummies = df.copy()
    if 'show_preview' not in st.session_state:
        st.session_state.show_preview = False
    
    # Botão de explicação
    with st.expander("ℹ️ Como funcionam as variáveis dummy?"):
        st.markdown("""
        **Variáveis dummy (one-hot encoding)** transformam categorias em colunas binárias.
        Cada categoria vira uma nova coluna com valores 0 ou 1.
        """)
    
    # Selecionar colunas categóricas
    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not colunas_categoricas:
        st.session_state.dummies = True
        # Botão para ir para próxima página (quando não há colunas categóricas)
        if st.button("Ir para Próxima Etapa"):
            st.session_state.pagina = 'Data config'
            st.rerun()
        return df
    
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas para criar dummy:",
        options=colunas_categoricas,
        default=colunas_categoricas
    )
    
    # Opções avançadas
    with st.expander("⚙️ Opções avançadas"):
        drop_first = st.checkbox("Remover primeira categoria", value=True)
    
    # Aplicar transformação
    if st.button("Criar Variáveis Dummy"):
        try:
            df_dummies = df.copy()
            
            # Verificar cardinalidade
            high_card = [col for col in colunas_selecionadas if df[col].nunique() > 15]
            if high_card:
                st.warning(f"Cuidado com alta cardinalidade em: {', '.join(high_card)}")
            
            # Criar dummies
            df_dummies = pd.get_dummies(
                df_dummies,
                columns=colunas_selecionadas,
                drop_first=drop_first
            )
            
            st.session_state.df_temp = df_dummies.copy()
            st.session_state.show_preview = True
            st.session_state.df = st.session_state.df_temp.copy()
            st.success("Transformação aplicada! Visualize o resultado abaixo.")
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")
    
    # Mostrar prévia após transformação
    if st.session_state.show_preview:
        st.subheader("Prévia dos dados (5 primeiros registros)")
        st.dataframe(st.session_state.df_temp.head())
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏪ Desfazer"):
                st.session_state.df = st.session_state.df_original_dummies.copy()
                st.session_state.df_temp = st.session_state.df_original_dummies.copy()
                st.rerun()
        
        with col2:
            if st.button("💾 Gravar Alterações"):
                st.session_state.dummies = True
                st.success("✅ Alterações gravadas com sucesso!")
    
    # Botão para ir para próxima página (sempre visível no final)
    st.markdown("---")  # Linha separadora
    if st.button("Ir para Próxima Etapa"):
        st.session_state.pagina = 'Data config'
        st.rerun()
    
    return st.session_state.df if 'df' in st.session_state else df