import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Análise RFV - Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .rfv-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def gerar_dados_exemplo():
    """Gera dados de exemplo no formato do CSV fornecido"""
    np.random.seed(42)
    
    # Gerar dados no formato: ID_cliente, CodigoCompra, DiaCompra, ValorTotal
    n_clientes = 200
    dados = []
    
    # Data base para gerar compras nos últimos 2 anos
    data_base = datetime(2023, 12, 31)
    
    for cliente_id in range(12000, 12000 + n_clientes):
        # Número aleatório de compras por cliente (1 a 20)
        n_compras = np.random.randint(1, 21)
        
        for compra_num in range(n_compras):
            # Código da compra (sequencial)
            codigo_compra = 500000 + (cliente_id - 12000) * 100 + compra_num
            
            # Data da compra (últimos 730 dias)
            dias_atras = np.random.randint(1, 731)
            dia_compra = data_base - timedelta(days=dias_atras)
            
            # Valor total da compra
            valor_total = np.random.lognormal(5.5, 0.8)  # Valores similares ao exemplo
            
            dados.append({
                'ID_cliente': cliente_id,
                'CodigoCompra': codigo_compra,
                'DiaCompra': dia_compra,
                'ValorTotal': round(valor_total, 2)
            })
    
    return pd.DataFrame(dados)

def calcular_rfv(df, data_referencia=None):
    """Calcula as métricas RFV para cada cliente usando as colunas do CSV"""
    if data_referencia is None:
        data_referencia = df['DiaCompra'].max()
    
    # Agrupar por ID_cliente
    rfv = df.groupby('ID_cliente').agg({
        'DiaCompra': ['max', 'count'],
        'ValorTotal': ['sum', 'mean']
    }).reset_index()
    
    # Flatten column names
    rfv.columns = ['ID_cliente', 'ultima_compra', 'frequencia', 'valor_total', 'ticket_medio']
    
    # Calcular recência (dias desde a última compra)
    rfv['recencia'] = (data_referencia - rfv['ultima_compra']).dt.days
    
    return rfv

def criar_segmentos_rfv(df):
    """Cria segmentos RFV baseado em quintis"""
    # Calcular quintis (invertido para recência - menor é melhor)
    df['R_score'] = pd.qcut(df['recencia'].rank(method='first', ascending=False), 5, labels=[5,4,3,2,1])
    df['F_score'] = pd.qcut(df['frequencia'].rank(method='first'), 5, labels=[1,2,3,4,5])
    df['V_score'] = pd.qcut(df['valor_total'].rank(method='first'), 5, labels=[1,2,3,4,5])
    
    # Criar score RFV
    df['RFV_score'] = df['R_score'].astype(str) + df['F_score'].astype(str) + df['V_score'].astype(str)
    
    # Definir segmentos
    def definir_segmento(row):
        r, f, v = int(row['R_score']), int(row['F_score']), int(row['V_score'])
        
        if r >= 4 and f >= 4 and v >= 4:
            return "Champions"
        elif r >= 3 and f >= 3 and v >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New Customers"
        elif r <= 2 and f >= 3:
            return "At Risk"
        elif r <= 1 and f <= 2:
            return "Lost Customers"
        elif v >= 4:
            return "Big Spenders"
        else:
            return "Others"
    
    df['segmento'] = df.apply(definir_segmento, axis=1)
    
    return df

# Interface Principal
st.markdown('<h1 class="main-header">📊 Análise RFV - Customer Analytics</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    opcao_dados = st.radio(
        "Fonte dos Dados:",
        ["Carregar dados.csv", "Gerar dados de exemplo", "Upload de arquivo"]
    )
    
    if opcao_dados == "Upload de arquivo":
        uploaded_file = st.file_uploader(
            "Escolha um arquivo CSV",
            type=['csv'],
            help="O arquivo deve conter: ID_cliente, CodigoCompra, DiaCompra, ValorTotal"
        )
    elif opcao_dados == "Carregar dados.csv":
        st.info("📁 Carregando arquivo: ./input/dados.csv")
        if st.button("🔄 Recarregar dados"):
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 Sobre RFV")
    st.markdown("""
    **Recência (R)**: Há quanto tempo o cliente fez a última compra
    
    **Frequência (F)**: Com que frequência o cliente compra
    
    **Valor (V)**: Quanto dinheiro o cliente gastou
    
    ---
    
    ### 📄 Formato do CSV
    - **ID_cliente**: Identificador do cliente
    - **CodigoCompra**: Código da compra
    - **DiaCompra**: Data da compra
    - **ValorTotal**: Valor total da compra
    """)

# Carregar dados
if opcao_dados == "Carregar dados.csv":
    try:
        with st.spinner("Carregando dados do arquivo ./input/dados.csv..."):
            df_compras = pd.read_csv('./dados.csv',
                                   infer_datetime_format=True,
                                   parse_dates=['DiaCompra'])
            st.success(f"✅ Arquivo carregado com sucesso! {len(df_compras):,} registros encontrados")
            
            # Mostrar preview dos dados
            with st.expander("👀 Preview dos dados carregados"):
                st.dataframe(df_compras.head(), use_container_width=True)
                st.write(f"**Shape dos dados:** {df_compras.shape[0]:,} linhas x {df_compras.shape[1]} colunas")
                st.write(f"**Período:** {df_compras['DiaCompra'].min().strftime('%d/%m/%Y')} até {df_compras['DiaCompra'].max().strftime('%d/%m/%Y')}")
                st.write(f"**Clientes únicos:** {df_compras['ID_cliente'].nunique():,}")
                
    except FileNotFoundError:
        st.error("❌ Arquivo './input/dados.csv' não encontrado!")
        st.info("💡 Certifique-se de que o arquivo está na pasta './input/dados.csv'")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
        st.stop()
        
elif opcao_dados == "Gerar dados de exemplo":
    with st.spinner("Gerando dados de exemplo..."):
        df_compras = gerar_dados_exemplo()
        st.success("✅ Dados de exemplo gerados com sucesso!")
        
        # Mostrar preview dos dados
        with st.expander("👀 Preview dos dados gerados"):
            st.dataframe(df_compras.head(), use_container_width=True)
            st.write(f"**Shape dos dados:** {df_compras.shape[0]:,} linhas x {df_compras.shape[1]} colunas")
            
else:  # Upload de arquivo
    if 'uploaded_file' in locals() and uploaded_file is not None:
        try:
            df_compras = pd.read_csv(uploaded_file,
                                   infer_datetime_format=True,
                                   parse_dates=['DiaCompra'])
            st.success("✅ Arquivo carregado com sucesso!")
            
            # Mostrar preview dos dados
            with st.expander("👀 Preview dos dados carregados"):
                st.dataframe(df_compras.head(), use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
            st.info("💡 Verifique se o arquivo tem as colunas: ID_cliente, CodigoCompra, DiaCompra, ValorTotal")
            st.stop()
    else:
        st.warning("⚠️ Por favor, faça upload de um arquivo CSV")
        st.stop()

# Processar dados RFV
if 'df_compras' in locals():
    with st.spinner("Calculando métricas RFV..."):
        df_rfv = calcular_rfv(df_compras)
        df_rfv_segmentado = criar_segmentos_rfv(df_rfv)
    
    # Análises adicionais específicas
    st.markdown("### 🔍 Análises Específicas dos Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Período dos Dados")
        data_min = df_compras['DiaCompra'].min()
        data_max = df_compras['DiaCompra'].max()
        periodo_dias = (data_max - data_min).days
        
        st.info(f"""
        **Data Mínima:** {data_min.strftime('%d/%m/%Y')}
        
        **Data Máxima:** {data_max.strftime('%d/%m/%Y')}
        
        **Período Total:** {periodo_dias:,} dias ({periodo_dias/365:.1f} anos)
        """)
    
    with col2:
        st.markdown("#### 📊 Estatísticas Gerais")
        st.info(f"""
        **Total de Compras:** {len(df_compras):,}
        
        **Clientes Únicos:** {df_compras['ID_cliente'].nunique():,}
        
        **Compras por Cliente:** {len(df_compras)/df_compras['ID_cliente'].nunique():.1f}
        
        **Valor Médio por Compra:** R$ {df_compras['ValorTotal'].mean():.2f}
        """)
    
    # Tabelas detalhadas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗓️ Recência - Última Compra por Cliente")
        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['DiasUltimaCompra'] = (data_max - df_recencia['DiaUltimaCompra']).dt.days
        df_recencia = df_recencia.sort_values('DiaUltimaCompra', ascending=False)
        
        st.dataframe(
            df_recencia.head(10).style.format({
                'DiaUltimaCompra': lambda x: x.strftime('%d/%m/%Y'),
                'DiasUltimaCompra': '{} dias'
            }),
            use_container_width=True
        )
        
        with st.expander("📋 Ver tabela completa de recência"):
            st.dataframe(df_recencia, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔄 Frequência - Compras por Cliente")
        df_frequencia = df_compras.groupby(by='ID_cliente', as_index=False)['CodigoCompra'].count()
        df_frequencia.columns = ['ID_cliente', 'FrequenciaCompras']
        df_frequencia = df_frequencia.sort_values('FrequenciaCompras', ascending=False)
        
        st.dataframe(df_frequencia.head(10), use_container_width=True)
        
        with st.expander("📋 Ver tabela completa de frequência"):
            st.dataframe(df_frequencia, use_container_width=True)
    
    # Valor total e médio por cliente
    st.markdown("#### 💰 Valor Total e Médio por Cliente")
    
    df_valor = df_compras.groupby(by='ID_cliente', as_index=False).agg({
        'ValorTotal': ['sum', 'mean', 'count']
    })
    df_valor.columns = ['ID_cliente', 'ValorTotal_Sum', 'ValorTotal_Mean', 'NumeroCompras']
    df_valor = df_valor.sort_values('ValorTotal_Sum', ascending=False)
    
    # Renomear colunas para melhor visualização
    df_valor_display = df_valor.copy()
    df_valor_display.columns = ['ID Cliente', 'Valor Total (R$)', 'Valor Médio (R$)', 'Nº Compras']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            df_valor_display.head(15).style.format({
                'Valor Total (R$)': 'R$ {:.2f}',
                'Valor Médio (R$)': 'R$ {:.2f}'
            }),
            use_container_width=True
        )
    
    with col2:
        # Gráfico de distribuição de valores
        fig_valor_dist = px.histogram(
            df_valor, x='ValorTotal_Sum', nbins=30,
            title="Distribuição Valor Total por Cliente",
            labels={'ValorTotal_Sum': 'Valor Total (R$)', 'count': 'Quantidade de Clientes'},
            color_discrete_sequence=['#667eea']
        )
        st.plotly_chart(fig_valor_dist, use_container_width=True)
    
    with st.expander("📋 Ver tabela completa de valores"):
        st.dataframe(df_valor_display, use_container_width=True)
    
    # Gráficos de distribuição das métricas específicas
    st.markdown("### 📈 Distribuições das Métricas Calculadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Distribuição de frequência
        fig_freq = px.histogram(
            df_frequencia, x='FrequenciaCompras', nbins=20,
            title="Distribuição - Frequência de Compras",
            labels={'FrequenciaCompras': 'Número de Compras', 'count': 'Quantidade de Clientes'},
            color_discrete_sequence=['#764ba2']
        )
        st.plotly_chart(fig_freq, use_container_width=True)
    
    with col2:
        # Distribuição de recência
        fig_rec = px.histogram(
            df_recencia, x='DiasUltimaCompra', nbins=30,
            title="Distribuição - Dias desde Última Compra",
            labels={'DiasUltimaCompra': 'Dias', 'count': 'Quantidade de Clientes'},
            color_discrete_sequence=['#f093fb']
        )
        st.plotly_chart(fig_rec, use_container_width=True)
    
    with col3:
        # Distribuição de ticket médio
        fig_ticket = px.histogram(
            df_valor, x='ValorTotal_Mean', nbins=30,
            title="Distribuição - Ticket Médio",
            labels={'ValorTotal_Mean': 'Ticket Médio (R$)', 'count': 'Quantidade de Clientes'},
            color_discrete_sequence=['#ffeaa7']
        )
        st.plotly_chart(fig_ticket, use_container_width=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f'<div class="metric-container"><h3>{len(df_rfv):,}</h3><p>Total de Clientes</p></div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f'<div class="metric-container"><h3>R$ {df_compras["ValorTotal"].sum():,.0f}</h3><p>Receita Total</p></div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f'<div class="metric-container"><h3>R$ {df_rfv["ticket_medio"].mean():.0f}</h3><p>Ticket Médio</p></div>',
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f'<div class="metric-container"><h3>{df_rfv["frequencia"].mean():.1f}</h3><p>Freq. Média</p></div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Distribuição dos Segmentos
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Distribuição dos Segmentos")
        segmentos_count = df_rfv_segmentado['segmento'].value_counts()
        
        fig_pie = px.pie(
            values=segmentos_count.values,
            names=segmentos_count.index,
            title="Distribuição de Clientes por Segmento",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Valor por Segmento")
        valor_por_segmento = df_rfv_segmentado.groupby('segmento')['valor_total'].sum().sort_values(ascending=True)
        
        fig_bar = px.bar(
            x=valor_por_segmento.values,
            y=valor_por_segmento.index,
            orientation='h',
            title="Receita Total por Segmento",
            color=valor_por_segmento.values,
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Análise RFV Detalhada
    st.markdown("### 🔍 Análise RFV Detalhada")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_r = px.histogram(
            df_rfv_segmentado, x='recencia', nbins=30,
            title="Distribuição - Recência (dias)",
            color_discrete_sequence=['#667eea']
        )
        st.plotly_chart(fig_r, use_container_width=True)
    
    with col2:
        fig_f = px.histogram(
            df_rfv_segmentado, x='frequencia', nbins=20,
            title="Distribuição - Frequência",
            color_discrete_sequence=['#764ba2']
        )
        st.plotly_chart(fig_f, use_container_width=True)
    
    with col3:
        fig_v = px.histogram(
            df_rfv_segmentado, x='valor_total', nbins=30,
            title="Distribuição - Valor Total",
            color_discrete_sequence=['#f093fb']
        )
        st.plotly_chart(fig_v, use_container_width=True)
    
    # Scatter Plot RFV
    st.markdown("### 🎨 Visualização 3D - RFV")
    
    fig_3d = px.scatter_3d(
        df_rfv_segmentado,
        x='recencia', y='frequencia', z='valor_total',
        color='segmento',
        title="Análise RFV em 3D - Clientes por Segmento",
        hover_data=['ID_cliente']
    )
    fig_3d.update_layout(height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Tabela dos Segmentos
    st.markdown("### 📋 Resumo dos Segmentos")
    
    # Tabela detalhada dos top clientes
    st.markdown("### 🏆 Top 10 Clientes por Valor")
    top_clientes = df_rfv_segmentado.nlargest(10, 'valor_total')[['ID_cliente', 'segmento', 'recencia', 'frequencia', 'valor_total', 'ticket_medio']]
    top_clientes.columns = ['ID Cliente', 'Segmento', 'Recência (dias)', 'Frequência', 'Valor Total (R$)', 'Ticket Médio (R$)']
    st.dataframe(top_clientes, use_container_width=True)
    
    # Download dos resultados
    st.markdown("### 💾 Download dos Resultados")
    
    csv_buffer = df_rfv_segmentado.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Análise RFV Completa (CSV)",
        data=csv_buffer,
        file_name=f"analise_rfv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 Análise RFV - Customer Analytics | Desenvolvido com ❤️ usando Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)