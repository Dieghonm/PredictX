import streamlit as st
import pandas as pd
import numpy as np


def split_data_by_percentage():
    val, test = st.columns(2)
    with val:
        val_val = st.slider(
            "Validação (%)", 
            min_value=0, max_value=30, value=15, step=5,
            help="Porcentagem de dados para validação"
        )
    with test:
        test_val = st.slider(
            "Teste (%)", 
            min_value=0, max_value=30, value=15, step=5,
            help="Porcentagem de dados para teste"
        )

    train_val = 100 - (val_val + test_val)
    st.success(f"✅ Seus dados serão divididos em treino: {train_val}%, validação: {val_val}%, teste: {test_val}%")
    
    return {
        "method": "percentage",
        "train": train_val,
        "validation": val_val,
        "test": test_val
    }

def split_data_by_column(df, colunas):
    colunas_temporais = [col for col in colunas if 
        pd.api.types.is_datetime64_any_dtype(df[col]) or
        'data' in col.lower() or 
        'date' in col.lower()
    ]

    col_divisao = st.selectbox(
        "Selecione a coluna para divisão:",
        options=colunas,
        index=colunas.index(colunas_temporais[0]) if colunas_temporais and colunas_temporais[0] in colunas else 0,
        help="Coluna que define a divisão (ex: 'split_column' com valores 'train', 'val', 'test')"
    )

    if col_divisao in colunas_temporais:
        return handle_temporal_split(df, col_divisao)
    else:
        return handle_categorical_split(col_divisao)

def handle_temporal_split(df, col_divisao):

    datas_formatadas =[data[3:] for data in df['data_ref'].unique()]

    # Usar um prefixo único para as chaves baseado no nome da coluna
    key_prefix = f"{col_divisao}_"
    
    train_end_idx = st.select_slider(
        "Selecione a data final para o período de treino:",
        options=range(len(datas_formatadas)),
        format_func=lambda x: datas_formatadas[x],
        value=len(datas_formatadas)-4 if len(datas_formatadas) >= 4 else len(datas_formatadas)-1,
        key=f"{key_prefix}train_slider"  # Chave única
    )
    train_end_date = datas_formatadas[train_end_idx]
    st.success(f"✅ Período de treino: de {datas_formatadas[0]} até {train_end_date}")

    # Garantir que o índice de início da validação/teste é válido
    val_test_start_idx = st.select_slider(
        "Selecione a data inicial para validação e teste:",
        options=range(train_end_idx+1, len(datas_formatadas)),
        format_func=lambda x: datas_formatadas[x],
        value=min(train_end_idx+1, len(datas_formatadas)-1),
        key=f"{key_prefix}val_test_slider" 
    )
    val_test_start_date = datas_formatadas[val_test_start_idx]

    return {
        "method": "temporal",
        "column": col_divisao,
        "train": {
            'start': datas_formatadas[0],
            'end': train_end_date
        },
        "validation": {
            'start': datas_formatadas[train_end_idx+1] if train_end_idx+1 < len(datas_formatadas) else train_end_date,
            'end': val_test_start_date
        },
        "test": {
            'start': val_test_start_date,
            'end': datas_formatadas[-1]
        }
    }


def handle_categorical_split(col_divisao):
    col1, col2, col3 = st.columns(3)
    with col1:
        train_val = st.text_input("Valor para Treino", "train")
    with col2:
        val_val = st.text_input("Valor para Validação", "val")
    with col3:
        test_val = st.text_input("Valor para Teste", "test")
    
    return {
        "method": col_divisao,
        "train": train_val,
        "validation": val_val,
        "test": test_val
    }

def data_splitting_options(df, colunas):
    with st.expander("✂️ **Divisão dos Dados (Train/Val/Test)**", expanded=True):
        metodo_divisao = st.radio(
            "Método de divisão:",
            options=["Por porcentagem", "Por coluna específica"],
            horizontal=True,
            help="Escolha como dividir seus dados em conjuntos de treino, validação e teste"
        )

        if metodo_divisao == "Por porcentagem":
            split= split_data_by_percentage()
        else:
            split= split_data_by_column(df, colunas)
        
        if st.button("Guardar divisão"):
            st.session_state.split = split
            st.rerun()
