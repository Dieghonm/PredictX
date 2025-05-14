import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def get_numeric_columns(df):
    """Retorna colunas numéricas do DataFrame"""
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

def detectar_outliers(df, coluna, iqr_factor=1.5):
    """
    Detecta outliers usando o método IQR (Intervalo Interquartil)
    
    Args:
        df: DataFrame pandas
        coluna: Nome da coluna para verificar
        iqr_factor: Fator multiplicador do IQR (padrão 1.5)
    
    Returns:
        Tuple: (limite_inferior, limite_superior, outliers_df)
    """
    if coluna not in df.columns:
        raise ValueError(f"Coluna '{coluna}' não encontrada no DataFrame")
    
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    iqr = q3 - q1
    
    limite_inferior = q1 - (iqr_factor * iqr)
    limite_superior = q3 + (iqr_factor * iqr)
    
    outliers = df[(df[coluna] < limite_inferior) | (df[coluna] > limite_superior)]
    
    return limite_inferior, limite_superior, outliers

def plot_outliers(df, coluna):
    """
    Gera visualizações para análise de outliers
    
    Args:
        df: DataFrame pandas
        coluna: Nome da coluna para visualizar
    
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Boxplot
    sns.boxplot(y=df[coluna], ax=ax1)
    ax1.set_title(f'Boxplot de {coluna}')
    
    # Histograma
    sns.histplot(df[coluna], kde=True, ax=ax2)
    ax2.set_title(f'Distribuição de {coluna}')
    
    plt.tight_layout()
    return fig

def handle_outliers(df, numeric_cols=None):
    """
    Interface para detecção e tratamento de outliers
    
    Args:
        df: DataFrame pandas
        numeric_cols: Lista de colunas numéricas (opcional)
    
    Returns:
        DataFrame tratado
    """
    if numeric_cols is None:
        numeric_cols = get_numeric_columns(df)
    
    if not numeric_cols:
        st.warning("Nenhuma coluna numérica encontrada para análise.")
        return df
    
    with st.expander("📊 Detecção de Outliers", expanded=True):
        st.header("Identificação de Outliers")

        coluna_analise = st.selectbox(
            "Selecione a coluna para análise:",
            options=numeric_cols[::-1],
            key="coluna_outlier"
        )
        
        if coluna_analise:
            try:
                lim_inf, lim_sup, outliers = detectar_outliers(df, coluna_analise)
                total_registros = len(df[coluna_analise])
                percent_outliers = min(round((len(outliers) / total_registros) * 100, 2), 100.00)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Limite inferior", f"{round(lim_inf, 2)}")
                    st.metric("Limite superior", f"{round(lim_sup, 2)}")
                with col2:
                    st.metric("Outliers encontrados", len(outliers))
                    st.metric("Percentual de outliers", f"{percent_outliers}%")
                if len(outliers):
                    # Visualização dos dados
                    st.pyplot(plot_outliers(df, coluna_analise))
                    
                    # Seção de ajuste de outliers
                    st.markdown("---")
                    st.subheader("🔧 Ajuste de Outliers")
                    
                    # Slider para ajuste percentual
                    percentual_desejado = st.slider(
                        "Percentual máximo de outliers a manter:",
                        min_value=0.0,
                        max_value=float(percent_outliers),
                        value=float(percent_outliers),
                        step=0.1,
                        format="%.1f%%",
                        help="Ajuste para controlar quantos outliers deseja manter"
                    )
                    
                    # Cálculo do novo limiar
                    sorted_values = df[coluna_analise].sort_values(ascending=False).values
                    n_outliers_desejados = max(0, int((percentual_desejado / 100) * total_registros))
                    
                    novo_limiar = (round(sorted_values[n_outliers_desejados], 2) 
                                if n_outliers_desejados < len(sorted_values) 
                                else round(lim_sup, 2))
                    
                    # Visualização do impacto
                    st.info(f"**Limiar calculado:** `{novo_limiar}` (removerá valores acima deste)")
                    
                    # Botão de aplicação
                    if st.button("✂️ Aplicar Corte", help="Remove os outliers conforme o limiar definido"):
                        df = df[df[coluna_analise] <= novo_limiar].copy()
                        st.session_state.df = df
                        st.success("Dados atualizados com sucesso!")
                        st.rerun()
                    
            except Exception as e:
                st.error(f"Erro ao analisar a coluna: {str(e)}")
    
    # Botão para finalizar
    if st.button("✅ Finalizar análise de outliers"):
        st.session_state.outlier_check = True
        st.rerun()

    return df