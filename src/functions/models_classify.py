from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def logistic_regression(df_treino, df_validation, df_teste, target):
    # Separando features e target
    X_train = df_treino.drop(columns=[target])
    y_train = df_treino[target]
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]
    
    X_test = df_teste.drop(columns=[target])
    y_test = df_teste[target]
    
    # Hiperparâmetros
    C = st.sidebar.slider("Parâmetro C", 0.01, 10.0, 1.0, 0.01)
    max_iter = st.sidebar.slider("Max Iterações", 100, 1000, 100, 50)
    
    # Criar e treinar modelo
    model = LogisticRegression(C=C, max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Exibir métricas
    _display_classification_metrics(y_train, y_val, y_test, 
                                  y_train_pred, y_val_pred, y_test_pred)
    
    # Coeficientes
    st.subheader("Coeficientes do Modelo")
    coef_df = pd.DataFrame({
        'Feature': X_train.columns,
        'Coeficiente': model.coef_[0]
    }).sort_values('Coeficiente', key=abs, ascending=False)
    
    st.dataframe(coef_df.style.format({'Coeficiente': '{:.4f}'}))
    
    # Matriz de confusão
    _plot_confusion_matrix(y_test, y_test_pred, "Regressão Logística")
    
    return model

def decision_tree(df_treino, df_validation, df_teste, target):
    # Separando features e target
    X_train = df_treino.drop(columns=[target])
    y_train = df_treino[target]
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]
    
    X_test = df_teste.drop(columns=[target])
    y_test = df_teste[target]
    
    # Hiperparâmetros
    max_depth = st.sidebar.slider("Profundidade Máxima", 1, 20, 5, 1)
    min_samples_split = st.sidebar.slider("Min Samples Split", 2, 20, 2, 1)
    min_samples_leaf = st.sidebar.slider("Min Samples Leaf", 1, 20, 1, 1)
    
    # Criar e treinar modelo
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Exibir métricas
    _display_classification_metrics(y_train, y_val, y_test, 
                                  y_train_pred, y_val_pred, y_test_pred)
    
    # Importância das features
    st.subheader("Importância das Features")
    importance_df = pd.DataFrame({
        'Feature': X_train.columns,
        'Importância': model.feature_importances_
    }).sort_values('Importância', ascending=False)
    
    st.dataframe(importance_df.style.format({'Importância': '{:.4f}'}))
    
    # Matriz de confusão
    _plot_confusion_matrix(y_test, y_test_pred, "Árvore de Decisão")
    
    return model

def random_forest(df_treino, df_validation, df_teste, target):
    # Separando features e target
    X_train = df_treino.drop(columns=[target])
    y_train = df_treino[target]
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]
    
    X_test = df_teste.drop(columns=[target])
    y_test = df_teste[target]
    
    # Hiperparâmetros
    n_estimators = st.sidebar.slider("Número de Árvores", 10, 200, 100, 10)
    max_depth = st.sidebar.slider("Profundidade Máxima", 1, 20, 10, 1)
    min_samples_split = st.sidebar.slider("Min Samples Split", 2, 20, 2, 1)
    
    # Criar e treinar modelo
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Exibir métricas
    _display_classification_metrics(y_train, y_val, y_test, 
                                  y_train_pred, y_val_pred, y_test_pred)
    
    # Importância das features
    st.subheader("Importância das Features")
    importance_df = pd.DataFrame({
        'Feature': X_train.columns,
        'Importância': model.feature_importances_
    }).sort_values('Importância', ascending=False)
    
    st.dataframe(importance_df.style.format({'Importância': '{:.4f}'}))
    
    # Matriz de confusão
    _plot_confusion_matrix(y_test, y_test_pred, "Random Forest")
    
    return model

def svm_model(df_treino, df_validation, df_teste, target):
    # Separando features e target
    X_train = df_treino.drop(columns=[target])
    y_train = df_treino[target]
    
    X_val = df_validation.drop(columns=[target])
    y_val = df_validation[target]
    
    X_test = df_teste.drop(columns=[target])
    y_test = df_teste[target]
    
    # Hiperparâmetros
    C = st.sidebar.slider("Parâmetro C (SVM)", 0.01, 10.0, 1.0, 0.01)
    kernel = st.sidebar.selectbox("Kernel", ['linear', 'rbf', 'poly', 'sigmoid'])
    
    # Criar e treinar modelo
    model = SVC(C=C, kernel=kernel, random_state=42)
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Exibir métricas
    _display_classification_metrics(y_train, y_val, y_test, 
                                  y_train_pred, y_val_pred, y_test_pred)
    
    # Matriz de confusão
    _plot_confusion_matrix(y_test, y_test_pred, "SVM")
    
    return model

def _display_classification_metrics(y_train, y_val, y_test, 
                                  y_train_pred, y_val_pred, y_test_pred):
    """Função auxiliar para exibir métricas de classificação"""
    
    # CSS customizado
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
    
    # Função para calcular métricas seguras
    def safe_metric(y_true, y_pred, metric_func, **kwargs):
        try:
            return metric_func(y_true, y_pred, **kwargs)
        except:
            return 0.0
    
    with col1:
        st.markdown('<div class="metric-section"><b>Treino</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Accuracy: {accuracy_score(y_train, y_train_pred):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Precision: {safe_metric(y_train, y_train_pred, precision_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Recall: {safe_metric(y_train, y_train_pred, recall_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">F1-Score: {safe_metric(y_train, y_train_pred, f1_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-section"><b>Validação</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Accuracy: {accuracy_score(y_val, y_val_pred):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Precision: {safe_metric(y_val, y_val_pred, precision_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Recall: {safe_metric(y_val, y_val_pred, recall_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">F1-Score: {safe_metric(y_val, y_val_pred, f1_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-section"><b>Teste</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Accuracy: {accuracy_score(y_test, y_test_pred):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Precision: {safe_metric(y_test, y_test_pred, precision_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">Recall: {safe_metric(y_test, y_test_pred, recall_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">F1-Score: {safe_metric(y_test, y_test_pred, f1_score, average="weighted"):.4f}</div>', 
                   unsafe_allow_html=True)

def _plot_confusion_matrix(y_true, y_pred, model_name):
    """Função auxiliar para plotar matriz de confusão"""
    st.subheader(f"Matriz de Confusão - {model_name}")
    
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predito')
    ax.set_ylabel('Real')
    ax.set_title(f'Matriz de Confusão - {model_name}')
    
    st.pyplot(fig)
    plt.close()