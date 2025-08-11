from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def deep_learning_regression(df_treino, df_validation, df_teste, target):
    """Rede Neural para Regressão usando MLPRegressor"""
    
    # Separando features e target
    X_train = df_treino.drop(columns=[target])
    y_train = df_treino[target]
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]
    
    X_test = df_teste.drop(columns=[target])
    y_test = df_teste[target]
    
    # Normalização dos dados (importante para redes neurais)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Configurações da rede neural
    st.subheader("Configurações da Rede Neural")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hidden_layers = st.selectbox(
            "Arquitetura das Camadas Ocultas",
            options=[(100,), (100, 50), (100, 100), (200, 100, 50), (300, 200, 100)],
            format_func=lambda x: f"{len(x)} camadas: {x}"
        )
        
        activation = st.selectbox("Função de Ativação", 
                                ['relu', 'tanh', 'logistic'])
        
        solver = st.selectbox("Algoritmo de Otimização", 
                            ['adam', 'lbfgs', 'sgd'])
    
    with col2:
        learning_rate = st.slider("Taxa de Aprendizado", 0.0001, 0.01, 0.001, 0.0001)
        max_iter = st.slider("Máximo de Iterações", 100, 1000, 200, 50)
        early_stopping = st.checkbox("Early Stopping", value=True)
    
    if st.button("Treinar Rede Neural"):
        with st.spinner("Treinando rede neural..."):
            
            # Criar modelo
            model = MLPRegressor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                solver=solver,
                learning_rate_init=learning_rate,
                max_iter=max_iter,
                early_stopping=early_stopping,
                validation_fraction=0.1,
                random_state=42
            )
            
            # Treinar modelo
            model.fit(X_train_scaled, y_train)
            
            # Fazer previsões
            y_train_pred = model.predict(X_train_scaled)
            y_val_pred = model.predict(X_val_scaled)
            y_test_pred = model.predict(X_test_scaled)
            
            # Exibir métricas
            _display_regression_metrics(y_train, y_val, y_test,
                                      y_train_pred, y_val_pred, y_test_pred)
            
            # Curva de aprendizado
            if hasattr(model, 'loss_curve_'):
                _plot_learning_curve(model.loss_curve_, "Deep Learning - Regressão")
            
            # Salvar modelo no session_state
            st.session_state.trained_model = model
            st.session_state.scaler = scaler
            
            st.success("Rede neural treinada com sucesso!")
    
    return None
