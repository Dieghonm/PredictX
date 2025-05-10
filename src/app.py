import streamlit as st
from paginas import configuracoes_page, data_page, planilha_page, graficos_page, opcoes_page

st.set_page_config(page_title="Scoragem de Crédito", layout="wide")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Data"
if "df" not in st.session_state:
    st.session_state.df = None

# Função para trocar de página
def ir_para(pagina_nome):
    st.session_state.pagina = pagina_nome

# Sidebar com botões
st.sidebar.title("📚 Navegação")
if st.sidebar.button("📂 Data"):
    ir_para("Data")
if st.sidebar.button("📊 configuracoes"):
    ir_para("configuracoes")
if st.sidebar.button("📊 Planilha"):
    ir_para("Planilha")
if st.sidebar.button("📈 Gráficos"):
    ir_para("Gráficos")
if st.sidebar.button("⚙️ Opções"):
    ir_para("Opções")

# Renderiza a página correta
pagina_atual = st.session_state.pagina
if pagina_atual == "Data":
    data_page.mostrar()
elif pagina_atual == "Planilha":
    planilha_page.mostrar()
elif pagina_atual == "Gráficos":
    graficos_page.mostrar()
elif pagina_atual == "Opções":
    opcoes_page.mostrar()
elif pagina_atual == "configuracoes":
    configuracoes_page.mostrar()

