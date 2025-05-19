import streamlit as st

def spinner_personalizado(texto="Processando..."):
    """Cria um spinner visual personalizado que pode ser removido com certeza"""
    container = st.empty()
    container.markdown(f"""
    <style>
        .spinner {{
            border: 5px solid #f3f3f3;
            border-top: 5px solid #4a8bfc;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    <div style='text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-bottom: 20px;'>
        <div class="spinner"></div>
        <h3 style='color: #4a8bfc; margin-top: 15px;'>{texto}</h3>
    </div>
    """, unsafe_allow_html=True)
    return container
