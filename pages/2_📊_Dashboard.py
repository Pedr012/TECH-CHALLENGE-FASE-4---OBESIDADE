import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Análise de Dados",
    page_icon="📊",
    layout="wide"
)

# Cache dos dados
@st.cache_data
def load_data():
    """Carrega os dados processados"""
    data_path = Path("data/processed/obesity_data_clean.csv")
    df = pd.read_csv(data_path)
    return df

def main():
    st.title("📊 Dashboard - Análise de Obesidade")
    st.markdown("### Insights e Visualizações dos Dados")
    
    st.divider()
    
    # Carregar dados
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return
    
    # Sidebar - Filtros
    with st.sidebar:
        st.header("🔍 Filtros")
        
        # Filtro de gênero
        gender_filter = st.multiselect(
            "Gênero",
            options=[0, 1],
            default=[0, 1],
            format_func=lambda x: 'Feminino' if x == 0 else 'Masculino'
        )
        
        # Filtro de idade
        age_range = st.slider(
            "Faixa Etária",
            int(df['age'].min()),
            int(df['age'].max()),
            (int(df['age'].min()), int(df['age'].max()))
        )
        
        st.divider()
        st.caption(f"**Total de registros:** {len(df)}")
    
    # Aplicar filtros
    df_filtered = df[
        (df['gender'].isin(gender_filter)) &
        (df['age'].between(age_range[0], age_range[1]))
    ]
    
    # Métricas principais
    st.header("📈 Visão Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Pacientes",
            f"{len(df_filtered):,}",
            delta=f"{len(df_filtered) - len(df)} (filtro)"
        )
    
    with col2:
        avg_age = df_filtered['age'].mean()
        st.metric(
            "Idade Média",
            f"{avg_age:.1f} anos"
        )
    
    with col3:
        avg_bmi = df_filtered['bmi'].mean()
        st.metric(
            "IMC Médio",
            f"{avg_bmi:.2f}"
        )
    
    with col4:
        obesity_rate = (df_filtered['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(df_filtered)) * 100
        st.metric(
            "Taxa de Obesidade",
            f"{obesity_rate:.1f}%"
        )
    
    st.divider()
    
    # Distribuição de Obesidade
    st.header("📊 Distribuição dos Níveis de Obesidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        obesity_counts = df_filtered['obesity_level'].value_counts().reset_index()
        obesity_counts.columns = ['Nível', 'Quantidade']
        
        fig_bar = px.bar(
            obesity_counts,
            x='Nível',
            y='Quantidade',
            title='Contagem por Nível de Obesidade',
            color='Quantidade',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Gráfico de pizza
        fig_pie = px.pie(
            obesity_counts,
            values='Quantidade',
            names='Nível',
            title='Proporção dos Níveis de Obesidade'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # Análise por Gênero
    st.header("👥 Análise Demográfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por gênero
        df_filtered['gender_label'] = df_filtered['gender'].map({0: 'Feminino', 1: 'Masculino'})
        gender_obesity = pd.crosstab(df_filtered['gender_label'], df_filtered['obesity_level'])
        
        fig_gender = go.Figure()
        for obesity_level in gender_obesity.columns:
            fig_gender.add_trace(go.Bar(
                name=obesity_level,
                x=gender_obesity.index,
                y=gender_obesity[obesity_level]
            ))
        
        fig_gender.update_layout(
            title='Distribuição de Obesidade por Gênero',
            barmode='group',
            xaxis_title='Gênero',
            yaxis_title='Quantidade'
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Distribuição de idade
        fig_age = px.histogram(
            df_filtered,
            x='age',
            nbins=30,
            title='Distribuição de Idade',
            color_discrete_sequence=['#636EFA']
        )
        fig_age.update_layout(
            xaxis_title='Idade',
            yaxis_title='Frequência'
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    st.divider()
    
    # Análise de Hábitos
    st.header("🍽️ Análise de Hábitos Alimentares e Estilo de Vida")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Consumo de vegetais vs Obesidade
        fig_fcvc = px.box(
            df_filtered,
            x='obesity_level',
            y='vegetable_consumption_freq',
            title='Consumo de Vegetais por Nível de Obesidade',
            color='obesity_level'
        )
        fig_fcvc.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_fcvc, use_container_width=True)
    
    with col2:
        # Atividade física vs Obesidade
        fig_faf = px.box(
            df_filtered,
            x='obesity_level',
            y='physical_activity_freq',
            title='Frequência de Atividade Física por Nível de Obesidade',
            color='obesity_level'
        )
        fig_faf.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_faf, use_container_width=True)
    
    st.divider()
    
    # Correlações
    st.header("🔗 Análise de Correlações")
    
    # Selecionar apenas colunas numéricas
    numeric_cols = ['age', 'height', 'weight', 'bmi']
    correlation_matrix = df_filtered[numeric_cols].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title='Matriz de Correlação entre Variáveis Numéricas',
        color_continuous_scale='RdBu_r',
        aspect='auto',
        labels=dict(color='Correlação')
    )
    fig_corr.update_layout(
        xaxis_title='',
        yaxis_title=''
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.divider()
    
    # Insights
    st.header("💡 Principais Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Padrões Identificados:**
        - Forte correlação entre peso, altura e IMC
        - Indivíduos com maior atividade física tendem a ter menor IMC
        - Consumo regular de vegetais associado a níveis menores de obesidade
        """)
        
        st.success("""
        **Fatores Protetores:**
        - Atividade física regular (FAF alto)
        - Consumo frequente de vegetais (FCVC alto)
        - Ingestão adequada de água (CH2O alto)
        - Menor tempo em dispositivos eletrônicos
        """)
    
    with col2:
        st.warning("""
        **Fatores de Risco:**
        - Histórico familiar de sobrepeso
        - Consumo frequente de alimentos calóricos
        - Baixa frequência de atividade física
        - Uso excessivo de transporte motorizado
        """)
        
        st.error("""
        **Alertas Importantes:**
        - Obesidade Tipo II e III requerem intervenção médica
        - Combinação de múltiplos fatores de risco
        - Necessidade de mudanças no estilo de vida
        """)
    
    st.divider()
    
    # Performance do Modelo
    st.header("🎯 Performance do Modelo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Acurácia", "93.2%")
        st.caption("Precisão geral do modelo")
    
    with col2:
        st.metric("AUC-ROC", "0.997")
        st.caption("Excelente capacidade discriminatória")
    
    with col3:
        st.metric("F1-Score", "93.1%")
        st.caption("Balanceamento entre precisão e recall")
    
    st.divider()
    
    # Rodapé
    st.caption("Dashboard desenvolvido com Streamlit e Plotly • Tech Challenge Fase 4 • 2024")

if __name__ == "__main__":
    main()
