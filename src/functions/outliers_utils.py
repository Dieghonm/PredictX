import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    iqr = q3 - q1
    
    limite_inferior = q1 - (iqr_factor * iqr)
    limite_superior = q3 + (iqr_factor * iqr)
    
    outliers = df[(df[coluna] < limite_inferior) | (df[coluna] > limite_superior)]
    
    return limite_inferior, limite_superior, outliers

def verificar_outliers(df):
    """
    Verifica outliers em todas as colunas numéricas do DataFrame
    
    Args:
        df: DataFrame pandas
    
    Returns:
        None (apenas imprime os resultados)
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    if len(numeric_cols) == 0:
        print("Nenhuma coluna numérica encontrada.")
        return
    
    print("🔍 Análise de Outliers (Método IQR)")
    print("="*50)
    
    for col in numeric_cols:
        try:
            lim_inf, lim_sup, outliers = detectar_outliers(df, col)
            n_outliers = len(outliers)
            
            print(f"\nColuna: {col}")
            print(f"- Limite inferior: {lim_inf:.4f}")
            print(f"- Limite superior: {lim_sup:.4f}")
            print(f"- Número de outliers: {n_outliers} ({n_outliers/len(df):.2%})")
            
            if n_outliers > 0:
                print("\nExemplos de outliers:")
                print(outliers[[col]].sort_values(col).head(5).to_string())
                
                print("\nEstatísticas dos outliers:")
                print(f"- Mínimo: {outliers[col].min():.4f}")
                print(f"- Máximo: {outliers[col].max():.4f}")
                print(f"- Média: {outliers[col].mean():.4f}")
                
        except Exception as e:
            print(f"Erro ao processar coluna {col}: {str(e)}")
    
    print("\n✅ Análise concluída!")

def plot_outliers(df, coluna):
    """
    Gera visualizações para análise de outliers
    
    Args:
        df: DataFrame pandas
        coluna: Nome da coluna para visualizar
    """
    plt.figure(figsize=(12, 6))
    
    # Boxplot
    plt.subplot(1, 2, 1)
    sns.boxplot(y=df[coluna])
    plt.title(f'Boxplot de {coluna}')
    
    # Histograma
    plt.subplot(1, 2, 2)
    sns.histplot(df[coluna], kde=True)
    plt.title(f'Distribuição de {coluna}')
    
    plt.tight_layout()
    plt.show()