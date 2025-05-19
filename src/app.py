import streamlit as st
from modules import (
    data_page,
    planilha_page,
    graficos_page,
    opcoes_page,
    testes_page,
    data_config
)

# Configurações iniciais da página
def configurar_pagina():
    st.set_page_config(
        page_title="PredictX",
        layout="wide",
        page_icon="📊"
    )

# Inicialização do estado da sessão
def inicializar_session_state():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Data"
    if "df" not in st.session_state:
        st.session_state.df = None
    if 'outlier_check' not in st.session_state:
        st.session_state.outlier_check = False
    if 'target' not in st.session_state:
        st.session_state.target = None
    if 'split' not in st.session_state:
        st.session_state.split = None
    if 'datetime' not in st.session_state:
        st.session_state.datetime = False
    if 'normalization' not in st.session_state:
        st.session_state.normalization = False


# Navegação entre páginas
def navegacao_sidebar():
    st.sidebar.title("📚 Navegação")
    
    # Dicionário de páginas para facilitar a manutenção
    paginas = {
        "📂 Data": "Data",
        "🛠️ Data config" : "Data config",
        "📊 Planilha": "Planilha",
        "📈 Gráficos": "Gráficos",
        "🔧 Opções": "Opções",
        "🔧 Testes": "Testes"
    }
    
    for texto_botao, pagina_nome in paginas.items():
        if st.sidebar.button(texto_botao):
            st.session_state.pagina = pagina_nome

# Renderização da página atual
def renderizar_pagina():
    paginas = {
        "Data": data_page.mostrar,
        "Data config": data_config.mostrar,
        "Planilha": planilha_page.mostrar,
        "Gráficos": graficos_page.mostrar,
        "Opções": opcoes_page.mostrar,
        "Testes": testes_page.mostrar
    }
    
    pagina_atual = st.session_state.pagina
    if pagina_atual in paginas:
        paginas[pagina_atual]()
    else:
        st.warning(f"Página '{pagina_atual}' não encontrada. Redirecionando para a página inicial.")
        st.session_state.pagina = "Data"
        data_page.mostrar()

# Função principal
def main():
    configurar_pagina()
    inicializar_session_state()
    navegacao_sidebar()
    renderizar_pagina()

if __name__ == "__main__":
    main()

