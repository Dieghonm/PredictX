import streamlit as st


def check_duplicates(df):
    """
    Verifica e exibe informações sobre linhas duplicadas no DataFrame
    Retorna o DataFrame sem duplicatas se o usuário optar por removê-las
    """
    total_duplicados = df.duplicated().sum()
    
    if total_duplicados > 0:
        with st.expander("🔍 **Verificação de Dados Duplicados**", expanded=True):
            st.warning(f"⚠️ **{total_duplicados} linhas duplicadas** encontradas no dataset")
            
            # Opções para o usuário
            option = st.radio(
                "Como deseja tratar os dados duplicados?",
                options=[
                    "Remover todas as linhas duplicadas (manter apenas a primeira ocorrência)",
                    "Remover todas as linhas duplicadas (manter apenas a última ocorrência)",
                    "Manter apenas linhas que NÃO são duplicatas (remover TODAS as ocorrências de duplicatas)"
                ],
                index=0
            )
            
            if st.button("Aplicar Tratamento de Duplicatas"):
                if option == "Remover todas as linhas duplicadas (manter apenas a primeira ocorrência)":
                    df = df.drop_duplicates(keep='first')
                elif option == "Remover todas as linhas duplicadas (manter apenas a última ocorrência)":
                    df = df.drop_duplicates(keep='last')
                elif option == "Manter apenas linhas que NÃO são duplicatas (remover TODAS as ocorrências de duplicatas)":
                    df = df.drop_duplicates(keep=False)
                
                st.success(f"✅ {total_duplicados - df.duplicated().sum()} linhas duplicadas removidas")
                st.session_state.df = df
                st.rerun()

            # Mostrar estatísticas dos duplicados
            dup_stats = df[df.duplicated(keep=False)].groupby(df.columns.tolist()).size().reset_index(name='Contagem')
            st.dataframe(dup_stats.sort_values('Contagem', ascending=False))
    
    return df
