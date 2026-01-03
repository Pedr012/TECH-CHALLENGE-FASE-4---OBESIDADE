import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏥 Sistema Preditivo de Obesidade")
st.markdown("### Previsão de Risco Utilizando Machine Learning")

st.divider()

# Seção: Sobre o Sistema
st.header("📋 Sobre o Sistema")
st.write("""
Este sistema utiliza **Machine Learning** para prever o nível de obesidade com base em 
características demográficas, hábitos alimentares e estilo de vida do paciente.
""")

st.divider()

# Métricas de Performance
st.header("📊 Performance do Modelo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Acurácia",
        value="93.2%",
        delta="Alta precisão"
    )

with col2:
    st.metric(
        label="AUC-ROC",
        value="0.997",
        delta="Excelente"
    )

with col3:
    st.metric(
        label="Classes",
        value="7",
        delta="Categorias"
    )

with col4:
    st.metric(
        label="Amostras",
        value="2,111",
        delta="Dataset"
    )

st.divider()

# Funcionalidades
st.header("🚀 Funcionalidades")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Predição Individual")
    st.write("""
    - Entrada de dados do paciente
    - Previsão instantânea do nível de obesidade
    - Probabilidades por classe
    - Recomendações personalizadas
    """)

with col2:
    st.subheader("📈 Dashboard Analítico")
    st.write("""
    - Visualizações interativas dos dados
    - Distribuição das classes de obesidade
    - Análise de características relevantes
    - Insights sobre padrões identificados
    """)

st.divider()

# Classificações de Obesidade
st.header("📌 Níveis de Obesidade")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("**Peso Insuficiente**")
    st.caption("IMC < 18.5")
    
    st.success("**Peso Normal**")
    st.caption("18.5 ≤ IMC < 25")

with col2:
    st.warning("**Sobrepeso Nível I**")
    st.caption("25 ≤ IMC < 27")
    
    st.warning("**Sobrepeso Nível II**")
    st.caption("27 ≤ IMC < 30")

with col3:
    st.error("**Obesidade Tipo I**")
    st.caption("30 ≤ IMC < 35")
    
    st.error("**Obesidade Tipo II**")
    st.caption("35 ≤ IMC < 40")
    
    st.error("**Obesidade Tipo III**")
    st.caption("IMC ≥ 40")

st.divider()

# Instruções de navegação
st.info("""
**💡 Como usar:**
- Use a **barra lateral** para navegar entre as páginas
- Acesse **Predição** para realizar diagnósticos individuais
- Explore o **Dashboard** para visualizar insights dos dados
""")

# Rodapé
st.divider()
st.caption("Sistema desenvolvido com Streamlit • Tech Challenge Fase 4 • 2025")
