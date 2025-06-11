import streamlit as st
import pandas as pd

from functions import (
   models_regression,
)

def _setup_page_config():
    """Configurações de estilo da página."""
    st.markdown("""
        <style>
            .stButton>button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

def mostrar():
    st.title("🤖 Modelagem de Dados")
    _setup_page_config()
    
    if st.session_state.df is not None:
        if st.session_state.df_treino is not None:
            df_treino = st.session_state.df_treino.copy()
            df_validation = st.session_state.df_validation.copy()
            df_teste = st.session_state.df_teste.copy()
            target = st.session_state.target
            st.subheader("Selecione o tipo de modelagem:")
            
            # Criando abas para cada categoria de modelagem
            tab1, tab2, tab3 = st.tabs(["📈 Regressão", "🔍 Classificação", "🧠 Redes Neurais"])
            
            with tab1:
                st.header("Modelos de Regressão")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Regressão Linear"):
                        st.session_state.modelo_selecionado = "Regressão Linear"
                        models_regression.linear_regression(df_treino, df_validation, df_teste, target)
                        st.success("Modelo de Regressão Linear selecionado!")
                        # Exemplo: rodar_regressao_linear()
                        
                with col2:
                    if st.button("Regressão Ridge"):
                        st.session_state.modelo_selecionado = "Regressão Ridge"
                        st.success("Modelo de Regressão Ridge selecionado!")
                        
                with col3:
                    if st.button("Regressão Lasso"):
                        st.session_state.modelo_selecionado = "Regressão Lasso"
                        st.success("Modelo de Regressão Lasso selecionado!")
            
            with tab2:
                st.header("Modelos de Classificação")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Regressão Logística"):
                        st.session_state.modelo_selecionado = "Regressão Logística"
                        st.success("Modelo de Regressão Logística selecionado!")
                        
                with col2:
                    if st.button("Árvores de Decisão"):
                        st.session_state.modelo_selecionado = "Árvores de Decisão"
                        st.success("Modelo de Árvores de Decisão selecionado!")
                        
                with col3:
                    if st.button("Random Forest"):
                        st.session_state.modelo_selecionado = "Random Forest"
                        st.success("Modelo de Random Forest selecionado!")
                        
                with col4:
                    if st.button("SVM"):
                        st.session_state.modelo_selecionado = "SVM"
                        st.success("Modelo de SVM selecionado!")
            
            with tab3:
                st.header("Redes Neurais")
                if st.button("Deep Learning"):
                    st.session_state.modelo_selecionado = "Deep Learning"
                    st.success("Modelo de Deep Learning selecionado!")
                    # Aqui você poderia adicionar opções adicionais para configuração da rede
                
            # Mostra o modelo selecionado (opcional)
            if 'modelo_selecionado' in st.session_state:
                st.sidebar.markdown(f"**Modelo selecionado:** {st.session_state.modelo_selecionado}")












        else:
            st.warning("⚠️ Siga a etapa de configurações dos dados na aba **Data config**.")

    else:
        
        st.warning("Por favor, carregue e prepare os dados primeiro.")
        st.warning("⚠️ Carregue os dados na aba **Data**.")