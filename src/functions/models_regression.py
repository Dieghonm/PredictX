from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import streamlit as st

def linear_regression(df_treino, df_validation, df_teste, target):    
    # Separando features e target
    X_train = df_treino.drop(columns=[target])  
    y_train = df_treino[target]     
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]           
    
    X_test = df_teste.drop(columns=[target])    
    y_test = df_teste[target]
    
    # Criar e treinar modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Fazer previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)

    # CSS customizado apenas para as métricas
    st.markdown("""
    <style>
    .metric-section {
        font-size: 12px !important;
    }
    .metric-value {
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Organizar em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-section"><b>Treino</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMSE: {np.sqrt(mean_squared_error(y_train, y_train_pred)):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">R²: {r2_score(y_train, y_train_pred):.4f}</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-section"><b>Validação</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMSE: {np.sqrt(mean_squared_error(y_val, y_val_pred)):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">R²: {r2_score(y_val, y_val_pred):.4f}</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-section"><b>Teste</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMSE: {np.sqrt(mean_squared_error(y_test, y_test_pred)):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">R²: {r2_score(y_test, y_test_pred):.4f}</div>', 
                   unsafe_allow_html=True)

    # Restante do código mantido com fontes normais
    st.subheader("Coeficientes do Modelo")
    coef_df = pd.DataFrame({
        'Feature': X_train.columns,
        'Coeficiente': model.coef_
    }).sort_values('Coeficiente', ascending=False)
    
    st.dataframe(coef_df.style.format({'Coeficiente': '{:.4f}'}))
    
    return model