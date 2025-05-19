import streamlit as st

def config_buttons():
    if (
        st.session_state.get("outlier_check", False) or
        st.session_state.get("datetime", False) or
        st.session_state.get("target", False) or
        st.session_state.get("split", False)
    ):
        with st.expander("Botões de configurações", expanded=True):
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.session_state.outlier_check:
                    if st.button("Outlier"):
                        st.session_state.outlier_check = False
            
            with col2:
                if st.session_state.datetime:
                    if st.button("Converter DateTime"):
                        st.session_state.datetime = False

            with col3:
                if st.session_state.normalization:            
                    if st.button("normalização"):
                        st.session_state.normalization = None
            
            with col4:
                if st.session_state.target:
                    if st.button("Novo target"):
                        st.session_state.target = None
            
            with col5:
                if st.session_state.split:            
                    if st.button("Alterar spliting"):
                        st.session_state.split = None










