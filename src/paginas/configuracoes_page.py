import streamlit as st
import pandas as pd

def mostrar():
    st.title("⚙️ Configurações do Modelo")

    if "df" not in st.session_state or st.session_state.df.empty:
        st.warning("⚠️ Nenhum dado carregado. Vá para a aba **'Data'**.")
        st.stop()

    df = st.session_state.df.copy()
    colunas = df.columns.tolist()
    total_linhas = len(df)
    dados_faltantes = df.isna().sum()
    dados_faltantes_pct = (dados_faltantes / total_linhas * 100).round(2)
    faltantes_df = pd.DataFrame({
        "Coluna": dados_faltantes.index,
        "Qtd. Faltantes": dados_faltantes.values,
        "% Faltantes": dados_faltantes_pct.values
    }).sort_values(by="% Faltantes", ascending=False)
    faltantes_df = faltantes_df[faltantes_df["Qtd. Faltantes"] > 0]

    if not faltantes_df.empty:
        with st.expander("❗ **Tratamento de variável missing**", expanded=True):
            st.warning(f"⚠️ **{len(faltantes_df)} colunas com dados faltantes**")
            st.dataframe(faltantes_df)

            if st.checkbox("Remover linhas com dados faltantes", key="remove_missing"):
                df = df.dropna()
                st.session_state.df = df
                st.rerun()


            coluna_preencher = st.selectbox(
                "Coluna para preencher missing:",
                faltantes_df["Coluna"].tolist(),
                key="coluna_preencher"
            )

            metodo = st.radio(
                "Método de preenchimento:",
                ["Zero", "Média", "Mediana", "Moda", "Valor Personalizado"],
                key="metodo_preenchimento"
            )

            valor_personalizado = None
            if metodo == "Valor Personalizado":
                valor_personalizado = st.text_input("Digite o valor personalizado", key="valor_custom")

            aplicar = st.button("Aplicar Preenchimento", key="botao_aplicar")

            if aplicar:
                if metodo == "Zero":
                    df[coluna_preencher] = df[coluna_preencher].fillna(0)
                elif metodo == "Média":
                    df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].mean())
                elif metodo == "Mediana":
                    df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].median())
                elif metodo == "Moda":
                    df[coluna_preencher] = df[coluna_preencher].fillna(df[coluna_preencher].mode()[0])
                elif metodo == "Valor Personalizado" and valor_personalizado:
                    df[coluna_preencher] = df[coluna_preencher].fillna(valor_personalizado)

                st.session_state.df = df
                st.rerun()
    else:
        st.success("✅ **Nenhum dado faltante encontrado!**")
        with st.expander("🔍 **Seleção da Variável Alvo (Target)**", expanded=True):
            st.markdown(
                "Selecione a coluna que contém o valor que seu modelo deve prever. "
                "Esta será a variável dependente na análise."
            )

            target_col = st.selectbox(
                "Variável alvo:",
                options=colunas,
                index=len(colunas) - 1,
                key="target_selectbox",
                help="Esta coluna será usada como o valor a ser previsto pelo modelo."
            )

            st.code(f"Valores únicos na coluna '{target_col}':\n{df[target_col].unique()[:10]}", language='python')

            if len(df[target_col].unique()) > 20:
                st.warning("⚠️ Esta coluna tem muitos valores únicos. Verifique se é realmente uma variável alvo adequada.")

        with st.expander("✂️ **Divisão dos Dados (Train/Val/Test)**", expanded=True):
            metodo_divisao = st.radio(
                "Método de divisão:",
                options=["Por porcentagem", "Por coluna específica"],
                horizontal=True,
                help="Escolha como dividir seus dados em conjuntos de treino, validação e teste"
            )

            if metodo_divisao == "Por porcentagem":
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

            else:
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

                if col_divisao in df:
                    if col_divisao in colunas_temporais:
                        st.info("Divisão temporal selecionada - escolha os intervalos de data para treino:")
                        datas_ordenadas = sorted(pd.to_datetime(df[col_divisao].dropna().unique()))
                        datas_formatadas = [data.strftime('%m/%Y') for data in datas_ordenadas]

                        data_ref = st.select_slider(
                            "Deslize para escolher uma data de referência:",
                            options=datas_formatadas,
                            value=datas_formatadas[-3] if len(datas_formatadas) >= 3 else datas_formatadas[-1],
                            key="target_slider"
                        )

                        st.success(f"✅ Data selecionada: {data_ref}")
                    else:
                        st.info(f"Valores encontrados na coluna: {', '.join(map(str, df[col_divisao].unique()))}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            train_val = st.text_input("Valor para Treino", "train")
                        with col2:
                            val_val = st.text_input("Valor para Validação", "val")
                        with col3:
                            test_val = st.text_input("Valor para Teste", "test")


        with st.expander("⚡ Configurações Avançadas"):
            random_state = st.number_input(
                "Random State", 
                min_value=0, value=42,
                help="Semente aleatória para reprodutibilidade"
            )
            shuffle = st.checkbox(
                "Embaralhar dados", 
                value=True,
                help="Se os dados devem ser embaralhados antes da divisão"
            )

        if st.button("💾 Salvar Todas as Configurações", type="primary"):
            config = {
                "target_col": target_col,
                "split_method": metodo_divisao,
                "random_state": random_state,
                "shuffle": shuffle
            }

            if metodo_divisao == "Por porcentagem":
                config.update({
                    "train_size": train_size / 100,
                    "val_size": val_size / 100,
                    "test_size": test_size / 100
                })
            else:
                config.update({
                    "split_column": col_divisao
                })
                if col_divisao in colunas_temporais:
                    config["date_reference"] = data_ref
                else:
                    config.update({
                        "train_val": train_val,
                        "val_val": val_val,
                        "test_val": test_val
                    })

            st.session_state.model_config = config
            st.toast("Configurações salvas com sucesso!", icon="✅")
            st.success("Configurações prontas para uso no modelo!")
            st.json(config)

        st.success(f"✅ Variável alvo selecionada: {target_col}")
        st.success(f"{val_size}")
        st.success(f"{test_size}")


        # guardados
        # st.success(f"{target_col}")