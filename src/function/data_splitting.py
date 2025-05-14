import streamlit as st
import pandas as pd

def split_data_by_percentage():
    val, test = st.columns(2)
    with val:
        val_size = st.slider(
            "Validação (%)", 
            min_value=0, max_value=30, value=15, step=5,
            help="Porcentagem de dados para validação"
        )
    with test:
        test_size = st.slider(
            "Teste (%)", 
            min_value=0, max_value=30, value=15, step=5,
            help="Porcentagem de dados para teste"
        )

    train_size = 100 - (val_size + test_size)
    st.success(f"✅ Seus dados serão divididos em treino: {train_size}%, validação: {val_size}%, teste: {test_size}%")
    
    return {
        "method": "percentage",
        "validation": val_size,
        "test": test_size,
        "train": train_size
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
    datas_ordenadas = sorted(pd.to_datetime(df[col_divisao].dropna().unique()))
    datas_formatadas = [data.strftime('%m/%Y') for data in datas_ordenadas]

    train_end_idx = st.select_slider(
        "Selecione a data final para o período de treino:",
        options=range(len(datas_formatadas)),
        format_func=lambda x: datas_formatadas[x],
        value=len(datas_formatadas)-4 if len(datas_formatadas) >= 4 else len(datas_formatadas)-1,
        key="train_slider"
    )
    train_end_date = datas_formatadas[train_end_idx]
    st.success(f"✅ Período de treino: de {datas_formatadas[0]} até {train_end_date}")

    val_test_start_idx = st.select_slider(
        "Selecione a data inicial para validação e teste:",
        options=range(train_end_idx+1, len(datas_formatadas)),
        format_func=lambda x: datas_formatadas[x],
        value=min(train_end_idx+1, len(datas_formatadas)-1),
        key="val_test_slider"
    )
    val_test_start_date = datas_formatadas[val_test_start_idx]

    return {
        "method": "temporal",
        "column": col_divisao,
        "train": {
            'start': datas_formatadas[0],
            'end': train_end_date
        },
        "validation_test": {
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
        "method": "categorical",
        "column": col_divisao,
        "train_val": train_val,
        "val_val": val_val,
        "test_val": test_val
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