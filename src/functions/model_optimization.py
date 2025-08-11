import pandas as pd
import streamlit as st
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from sklearn.utils import class_weight
import numpy as np

def optimization():
    with st.expander("❗ **Contagem e Porcentagem por Valor**", expanded=True):
        # Verificações de segurança
        if 'df_treino' not in st.session_state or 'target' not in st.session_state:
            st.error("Dados não carregados! Verifique o upload.")
            return
        
        if st.session_state.target not in st.session_state.df_treino.columns:
            st.error(f"Coluna '{st.session_state.target}' não encontrada!")
            return

        # --- SEÇÃO DE REMOÇÃO DE COLUNAS ---
        st.markdown("### 🗑️ Remoção de Colunas")
        
        # Lista das colunas disponíveis (exceto a target)
        colunas_disponiveis = [col for col in st.session_state.df_treino.columns if col != st.session_state.target]
        
        if colunas_disponiveis:
            # Multiselect para escolher colunas a remover
            colunas_para_remover = st.multiselect(
                "Selecione as colunas que deseja remover:",
                options=colunas_disponiveis,
                help="Selecione uma ou mais colunas que não serão utilizadas na modelagem"
            )
            
            if colunas_para_remover:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button("🗑️ Remover Colunas Selecionadas", type="primary"):
                        datasets_removidos = []
                        
                        # Remove as colunas do dataset de treino
                        st.session_state.df_treino = st.session_state.df_treino.drop(columns=colunas_para_remover)
                        datasets_removidos.append("treino")
                        
                        # Remove das demais bases se existirem
                        datasets_para_verificar = ['df_validation', 'df_teste', 'df_balanceado']
                        nomes_datasets = ['validação', 'teste', 'balanceado']
                        
                        for dataset_name, nome_display in zip(datasets_para_verificar, nomes_datasets):
                            if dataset_name in st.session_state:
                                colunas_remover_dataset = [col for col in colunas_para_remover 
                                                         if col in st.session_state[dataset_name].columns]
                                if colunas_remover_dataset:
                                    st.session_state[dataset_name] = st.session_state[dataset_name].drop(columns=colunas_remover_dataset)
                                    datasets_removidos.append(nome_display)
                        
                        datasets_texto = ", ".join(datasets_removidos)
                        st.success(f"✅ {len(colunas_para_remover)} coluna(s) removida(s) de {datasets_texto}: {', '.join(colunas_para_remover)}")
                        st.rerun()
                
                with col2:
                    # Mostra informações sobre os datasets disponíveis
                    datasets_info = ["treino"]
                    total_colunas = len(st.session_state.df_treino.columns)
                    
                    if 'df_validation' in st.session_state:
                        datasets_info.append("validação")
                    if 'df_teste' in st.session_state:
                        datasets_info.append("teste")
                    if 'df_balanceado' in st.session_state:
                        datasets_info.append("balanceado")
                    
                    st.info(f"📊 Após remoção, os datasets ({', '.join(datasets_info)}) terão {total_colunas} colunas")
        else:
            st.info("Todas as colunas (exceto a target) já foram removidas ou não há colunas disponíveis para remoção.")
        
        st.markdown("---")

        # Calcula contagem e porcentagem
        contagem = st.session_state.df_treino[st.session_state.target].value_counts(dropna=False)
        porcentagem = (contagem / contagem.sum()) * 100

        # Exibe detalhamento por valor
        st.markdown("---")
        st.write("**Detalhamento por valor:**")
        
        for valor, qtd in contagem.items():
            st.write(
                f"- Valor **{valor}**: {qtd} ocorrências "
                f"({porcentagem[valor]:.2f}%)"
            )

        # --- VERIFICAÇÃO DE BALANCEAMENTO ---
        st.markdown("---")
        st.subheader("🔧 Ajuste para Modelagem")

        # Identifica se há desbalanceamento (considerando <30% como minoritária)
        classe_minoritaria = porcentagem.idxmin()
        perc_minoritario = porcentagem.min()
        
        if perc_minoritario < 30:
            st.warning(f"⚠️ Classe minoritária ('{classe_minoritaria}') tem apenas {perc_minoritario:.2f}% de representação")
            
            # --- BOTÕES PARA MÉTODOS DE BALANCEAMENTO ---
            st.markdown("### 🛠 Métodos de Balanceamento")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Undersampling"):
                    rus = RandomUnderSampler(random_state=42)
                    X = st.session_state.df_treino.drop(columns=[st.session_state.target])
                    y = st.session_state.df_treino[st.session_state.target]
                    X_res, y_res = rus.fit_resample(X, y)
                    st.session_state.df_balanceado = pd.concat([X_res, y_res], axis=1)
                    st.success("Undersampling aplicado! Classe majoritária reduzida.")
            
            with col2:
                if st.button("Oversampling (SMOTE)"):
                    smote = SMOTE(random_state=42)
                    X = st.session_state.df_treino.drop(columns=[st.session_state.target])
                    y = st.session_state.df_treino[st.session_state.target]
                    X_res, y_res = smote.fit_resample(X, y)
                    st.session_state.df_balanceado = pd.concat([X_res, y_res], axis=1)
                    st.success("SMOTE aplicado! Classe minoritária aumentada.")
            
            with col3:
                if st.button("Peso de Classes"):
                    classes = np.unique(st.session_state.df_treino[st.session_state.target])
                    pesos = class_weight.compute_class_weight(
                        'balanced',
                        classes=classes,
                        y=st.session_state.df_treino[st.session_state.target]
                    )
                    st.session_state.pesos_classes = dict(zip(classes, pesos))
                    st.success(f"Pesos calculados: {st.session_state.pesos_classes}")
            
            # Mostra dados balanceados se aplicado
            if 'df_balanceado' in st.session_state:
                st.markdown("---")
                st.subheader("📊 Dados Balanceados")
                contagem_balanceada = st.session_state.df_balanceado[st.session_state.target].value_counts(normalize=True) * 100
                st.write("Nova distribuição:")
                st.write(contagem_balanceada.round(2))
                
                if st.button("Visualizar DataFrame Balanceado"):
                    st.dataframe(st.session_state.df_balanceado)
        
        else:
            st.success("✅ Distribuição balanceada. Nenhum ajuste necessário.")