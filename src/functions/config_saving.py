import streamlit as st

def save_config(target_col, metodo_divisao, split_config, random_state, shuffle):
    config = {
        "target_col": target_col,
        "split_method": metodo_divisao,
        "random_state": random_state,
        "shuffle": shuffle
    }

    if metodo_divisao == "Por porcentagem":
        config.update({
            "train_size": split_config["train"] / 100,
            "val_size": split_config["validation"] / 100,
            "test_size": split_config["test"] / 100
        })
    else:
        config.update({
            "split_column": split_config["column"]
        })
        if split_config["method"] == "temporal":
            config["train_date_range"] = split_config["train"]
            config["val_test_date_range"] = split_config["validation_test"]
        else:
            config.update({
                "train_val": split_config["train_val"],
                "val_val": split_config["val_val"],
                "test_val": split_config["test_val"]
            })

    st.session_state.model_config = config
    st.toast("Configurações salvas com sucesso!", icon="✅")
    st.success("Configurações prontas para uso no modelo!")
    st.json(config)