import streamlit as st
from modules import (
    configuracoes_page,
    data_page,
    planilha_page,
    graficos_page,
    opcoes_page
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

# Navegação entre páginas
def navegacao_sidebar():
    st.sidebar.title("📚 Navegação")
    
    # Dicionário de páginas para facilitar a manutenção
    paginas = {
        "📂 Data": "Data",
        "⚙️ Configurações": "Configuracoes",
        "📊 Planilha": "Planilha",
        "📈 Gráficos": "Gráficos",
        "🔧 Opções": "Opções"
    }
    
    for texto_botao, pagina_nome in paginas.items():
        if st.sidebar.button(texto_botao):
            st.session_state.pagina = pagina_nome

# Renderização da página atual
def renderizar_pagina():
    paginas = {
        "Data": data_page.mostrar,
        "Configuracoes": configuracoes_page.mostrar,
        "Planilha": planilha_page.mostrar,
        "Gráficos": graficos_page.mostrar,
        "Opções": opcoes_page.mostrar
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

