import pandas as pd
from sklearn.model_selection import train_test_split
import streamlit as st

def show_preprocessing_results():
    """Exibe os resultados do pré-processamento realizado."""
    with st.expander("📊 Resultados do Pré-processamento", expanded=True):
        df= st.session_state.df
        target = st.session_state.target
        split = st.session_state.split
        def toggle_botao():
            st.session_state.botao_clicado = not st.session_state.botao_clicado
        
        def toggle_gravar(df_treino, df_validation, df_teste):
            st.session_state.df_treino = df_treino
            st.session_state.df_validation = df_validation
            st.session_state.df_teste = df_teste

        if 'botao_clicado' not in st.session_state:
            st.session_state.botao_clicado = False
        
        if st.session_state.df_treino is not None:
            st.subheader("Remover colunas")
            
            # 1. Mostra o DataFrame atual
            st.write("DataFrame atual:", st.session_state.df_treino.head())
            
            # 2. Widget para selecionar colunas a remover
            colunas_para_remover = st.multiselect(
                "Selecione as colunas para remover:",
                options=st.session_state.df_treino.columns.tolist()
            )
            
            # 3. Botão para confirmar a remoção
            if st.button("Remover colunas selecionadas"):
                if colunas_para_remover:
                    # Remove as colunas selecionadas
                    st.session_state.df_treino = st.session_state.df_treino.drop(columns=colunas_para_remover)
                    st.session_state.df_validation = st.session_state.df_validation.drop(columns=colunas_para_remover)
                    st.session_state.df_teste = st.session_state.df_teste.drop(columns=colunas_para_remover)
                    st.success(f"Colunas removidas: {', '.join(colunas_para_remover)} => Clique em Modelagem para continuar")
                    st.rerun()  
                    st.session_state.clean_df = True
                else:
                    st.warning("Nenhuma coluna selecionada!")
            
        else:
            if st.session_state.botao_clicado:
                if split['method'] == 'temporal':
                    df['data'] = pd.to_datetime(df[split['column']], format='%d/%m/%Y')

                    data_corte = pd.to_datetime(split['train']['end'], format='%m/%Y')

                    df_treino = df[df['data'] <= data_corte].drop('data', axis=1)
                    st.write(f"**Total de Registros para Treino: {len(df_treino)}**")
                    st.dataframe(df_treino.head())

                    df_temp = df[df['data'] > data_corte]

                    data_corte2 = pd.to_datetime(split['validation']['end'], format='%m/%Y')

                    df_validation = df_temp[df_temp['data'] <= data_corte2].drop('data', axis=1)
                    st.write(f"**Total de Registros para Validação: {len(df_validation)}**")
                    st.dataframe(df_validation.head())

                    df_teste = df_temp[df_temp['data'] > data_corte2].drop('data', axis=1)
                    st.write(f"**Total de Registros para Teste: {len(df_teste)}**")            
                    st.dataframe(df_teste.head())
                    st.button("Gravar dados", on_click=toggle_gravar(df_treino, df_validation, df_teste))

                elif split['method'] == 'percentage':                
                    df_treino, temp_df = train_test_split(df, test_size=(100 - split['train'])/100, random_state=42)
                    proporcao_teste = split['test'] / (split['validation'] + split['test'])
                    df_validation, df_teste = train_test_split(temp_df, test_size=proporcao_teste, random_state=42)

                    st.write(f"**Total de Registros para Treino: {len(df_treino)}**")
                    st.dataframe(df_treino.head())
                    st.write(f"**Total de Registros para Validação: {len(df_validation)}**")
                    st.dataframe(df_validation.head())
                    st.write(f"**Total de Registros para Teste: {len(df_teste)}**")
                    st.dataframe(df_teste.head())
                    st.button("Gravar dados", on_click=toggle_gravar(df_treino, df_validation, df_teste))
                else:
                    st.subheader("Ainda nao implementado")
                
            else:
                if st.session_state.split['method'] == 'temporal':
                    # Mostra estatísticas básicas em datas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Registros", len(df))
                        st.metric("Split", 'Data')
                        st.metric("Treino ", f"{split['train']['start']} > {split['train']['end']} ")
                    
                    with col2:
                        st.metric("Total de Colunas", len(df.columns))
                        st.metric("Coluna", f"{split['column']}")
                        st.metric("Validacão ", f"{split['validation']['start']} > {split['validation']['end']} ")

                    with col3:
                        st.metric("Targuet", f"{target}")
                        st.metric(".", '.')
                        st.metric("Teste", f"{split['test']['start']} > {split['test']['end']} ")

                else:
                    # Mostra estatísticas básicas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total de Registros", len(df))
                        st.metric("Split", f"{split['method']}")
                    
                    with col2:
                        st.metric("Total de Colunas", len(df.columns))
                        st.metric("Treino ", f"{split['train']}%")

                    with col3:
                        st.metric("Targuet", f"{target}")
                        st.metric("Validacão / Teste", f"{split['validation']}% / {split['test']}%")    

                st.subheader("Amostra dos Dados Transformados")
                st.dataframe(df.head())

                st.button("Confirmar e dividir os dados", on_click=toggle_botao)
            
        # Opções para próxima etapa

        # if st.button("Salvar Pré-processamento e Continuar"):

        # if st.button("Salvar Pré-processamento e Continuar"):
        #     st.session_state.preprocessing_complete = True
        #     st.rerun()
