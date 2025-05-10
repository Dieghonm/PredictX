import pandas as pd

def preprocess_data(df):
    df = df.copy()
    # Ajuste este pipeline conforme suas variáveis
    df.fillna(0, inplace=True)
    df = pd.get_dummies(df)
    return df
