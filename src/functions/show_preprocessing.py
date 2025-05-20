import pandas as pd
import streamlit as st

def show_preprocessing_results():
    """Exibe os resultados do pré-processamento realizado."""
    with st.expander("📊 Resultados do Pré-processamento", expanded=True):
        df= st.session_state.df
        target = st.session_state.target
        split = st.session_state.split
        st.subheader("Resumo das Transformações")

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

        # Mostra amostra dos dados
        st.subheader("Amostra dos Dados Transformados")
        st.dataframe(df.head())
        
        # Mostra informações sobre valores nulos
        st.subheader("Valores Nulos")
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            st.warning("⚠️ O dataset contém valores nulos!")
            st.dataframe(null_counts[null_counts > 0].rename("Quantidade de Nulos"))
        else:
            st.success("✅ Nenhum valor nulo encontrado!")
        
        # Opções para próxima etapa
        if st.button("Salvar Pré-processamento e Continuar"):
            st.session_state.preprocessing_complete = True
            st.rerun()

def datetime_options(df):
    """Interface para seleção e processamento de colunas de data."""
    with st.expander("🔍 Formatar Data", expanded=True):
        date_columns = get_date_columns(df)
        
        if not date_columns:
            st.info("Nenhuma coluna com formato de data identificada.")
            return df
    
        selected_dates = st.multiselect(
            "Selecione colunas para converter para datetime:",
            options=date_columns,
            default=[date_columns[0]] if date_columns else []
        )
        
        if st.button("Converter colunas selecionadas"):
            if selected_dates:
                for col in selected_dates:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')
                    st.session_state.df = df
                st.success(f"Colunas convertidas para datetime (dd/mm/aaaa): {selected_dates}")
                st.rerun()
            else:
                st.warning("Nenhuma coluna selecionada para conversão.")
                
        st.dataframe(df.head())
        
        if st.button("Próxima Etapa: Visualizar Resultados"):
            st.session_state.show_results = True
            st.rerun()
                
    return df

