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
        # Heatmap de hábitos alimentares
        st.subheader("Padrões de Hábitos Alimentares")
        
        # Criar matriz de contagem para hábitos alimentares
        food_habits = ['vegetable_consumption_freq', 'water_intake', 'main_meals_per_day', 'food_between_meals']
        food_matrix = []
        food_labels = []
        
        for habit in food_habits:
            habit_dist = pd.crosstab(
                df_filtered['obesity_level'], 
                df_filtered[habit], 
                normalize='index'
            ) * 100
            
            # Obter categorias ordenadas
            if habit == 'vegetable_consumption_freq':
                categories = ['rarely', 'sometimes', 'always']
                label_prefix = 'Vegetais'
            elif habit == 'water_intake':
                categories = ['low_consumption', 'adequate_consumption', 'high_consumption']
                label_prefix = 'Água'
            elif habit == 'main_meals_per_day':
                categories = ['one_meal', 'two_meals', 'three_meals', 'four_or_more_meals']
                label_prefix = 'Refeições'
            else:
                categories = df_filtered[habit].unique()
                label_prefix = 'Lanches'
            
            for cat in categories:
                if cat in habit_dist.columns:
                    food_matrix.append(habit_dist[cat].values)
                    food_labels.append(f"{label_prefix}: {cat.replace('_', ' ').title()}")
        
        fig_food = go.Figure(data=go.Heatmap(
            z=food_matrix,
            x=habit_dist.index,
            y=food_labels,
            colorscale='RdYlGn',
            text=np.round(food_matrix, 1),
            texttemplate='%{text}%',
            textfont={"size": 9},
            colorbar=dict(title="% Pessoas")
        ))
        
        fig_food.update_layout(
            title='Distribuição de Hábitos Alimentares por Nível de Obesidade',
            xaxis_title='Nível de Obesidade',
            yaxis_title='Comportamento Alimentar',
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_food, use_container_width=True)
    
    with col2:
        # Heatmap de estilo de vida
        st.subheader("Padrões de Estilo de Vida")
        
        # Criar matriz de contagem para estilo de vida
        lifestyle_habits = ['physical_activity_freq', 'technology_use_time', 'transportation_mode', 'frequent_high_caloric_food']
        lifestyle_matrix = []
        lifestyle_labels = []
        
        for habit in lifestyle_habits:
            habit_dist = pd.crosstab(
                df_filtered['obesity_level'], 
                df_filtered[habit], 
                normalize='index'
            ) * 100
            
            # Obter categorias ordenadas
            if habit == 'physical_activity_freq':
                categories = ['sedentary', 'low_frequency', 'moderate_frequency', 'high_frequency']
                label_prefix = 'Atividade Física'
            elif habit == 'technology_use_time':
                categories = ['low_use', 'moderate_use', 'high_use']
                label_prefix = 'Tempo de Tela'
            elif habit == 'frequent_high_caloric_food':
                categories = [0, 1]
                label_prefix = 'Alimentos Calóricos'
            else:
                categories = df_filtered[habit].unique()
                label_prefix = 'Transporte'
            
            for cat in categories:
                if cat in habit_dist.columns:
                    lifestyle_matrix.append(habit_dist[cat].values)
                    if habit == 'frequent_high_caloric_food':
                        cat_label = 'Não' if cat == 0 else 'Sim'
                    else:
                        cat_label = str(cat).replace('_', ' ').title()
                    lifestyle_labels.append(f"{label_prefix}: {cat_label}")
        
        fig_lifestyle = go.Figure(data=go.Heatmap(
            z=lifestyle_matrix,
            x=habit_dist.index,
            y=lifestyle_labels,
            colorscale='RdYlGn_r',
            text=np.round(lifestyle_matrix, 1),
            texttemplate='%{text}%',
            textfont={"size": 9},
            colorbar=dict(title="% Pessoas")
        ))
        
        fig_lifestyle.update_layout(
            title='Distribuição de Hábitos de Estilo de Vida por Nível de Obesidade',
            xaxis_title='Nível de Obesidade',
            yaxis_title='Comportamento',
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_lifestyle, use_container_width=True)
    
    st.divider()
    
    # Análise de Fatores de Risco
    st.header("🔗 Análise de Fatores de Risco Combinados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Impacto de Fatores Combinados")
        
        # Criar combinações de fatores de risco
        risk_combinations = []
        obesity_rates = []
        
        # Cenário 1: Histórico familiar + Sedentarismo
        scenario_1 = df_filtered[
            (df_filtered['family_history_overweight'] == 1) & 
            (df_filtered['physical_activity_freq'] == 'sedentary')
        ]
        if len(scenario_1) > 0:
            obesity_rate_1 = (scenario_1['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(scenario_1)) * 100
            risk_combinations.append('Histórico Familiar +\nSedentarismo')
            obesity_rates.append(obesity_rate_1)
        
        # Cenário 2: Sem histórico + Atividade regular
        scenario_2 = df_filtered[
            (df_filtered['family_history_overweight'] == 0) & 
            (df_filtered['physical_activity_freq'].isin(['moderate_frequency', 'high_frequency']))
        ]
        if len(scenario_2) > 0:
            obesity_rate_2 = (scenario_2['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(scenario_2)) * 100
            risk_combinations.append('Sem Histórico +\nAtividade Regular')
            obesity_rates.append(obesity_rate_2)
        
        # Cenário 3: Alimentos calóricos + Sedentarismo
        scenario_3 = df_filtered[
            (df_filtered['frequent_high_caloric_food'] == 1) & 
            (df_filtered['physical_activity_freq'] == 'sedentary')
        ]
        if len(scenario_3) > 0:
            obesity_rate_3 = (scenario_3['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(scenario_3)) * 100
            risk_combinations.append('Alimentos Calóricos +\nSedentarismo')
            obesity_rates.append(obesity_rate_3)
        
        # Cenário 4: Vegetais raros + Baixa água
        scenario_4 = df_filtered[
            (df_filtered['vegetable_consumption_freq'] == 'rarely') & 
            (df_filtered['water_intake'] == 'low_consumption')
        ]
        if len(scenario_4) > 0:
            obesity_rate_4 = (scenario_4['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(scenario_4)) * 100
            risk_combinations.append('Poucos Vegetais +\nPouca Água')
            obesity_rates.append(obesity_rate_4)
        
        # Cenário 5: Múltiplos fatores protetores
        scenario_5 = df_filtered[
            (df_filtered['physical_activity_freq'].isin(['moderate_frequency', 'high_frequency'])) & 
            (df_filtered['vegetable_consumption_freq'].isin(['sometimes', 'always'])) &
            (df_filtered['water_intake'].isin(['adequate_consumption', 'high_consumption']))
        ]
        if len(scenario_5) > 0:
            obesity_rate_5 = (scenario_5['obesity_level'].isin(['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']).sum() / len(scenario_5)) * 100
            risk_combinations.append('Múltiplos Fatores\nProtetores')
            obesity_rates.append(obesity_rate_5)
        
        # Criar gráfico de barras
        fig_risk = go.Figure(data=[
            go.Bar(
                y=risk_combinations,
                x=obesity_rates,
                orientation='h',
                marker=dict(
                    color=obesity_rates,
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="% Obesidade")
                ),
                text=[f'{rate:.1f}%' for rate in obesity_rates],
                textposition='outside'
            )
        ])
        
        fig_risk.update_layout(
            title='Taxa de Obesidade por Combinação de Fatores',
            xaxis_title='% Pessoas com Obesidade',
            yaxis_title='Combinação de Fatores',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.subheader("Relação IMC, Idade e Atividade Física")
        
        # Criar scatter plot IMC vs Idade colorido por atividade física
        df_scatter = df_filtered.copy()
        
        # Adicionar pequeno jitter para melhor visualização (evita sobreposição exata)
        np.random.seed(42)
        df_scatter['age_jitter'] = df_scatter['age'] + np.random.uniform(-0.3, 0.3, len(df_scatter))
        df_scatter['bmi_jitter'] = df_scatter['bmi'] + np.random.uniform(-0.2, 0.2, len(df_scatter))
        
        # Criar label para alimentos calóricos (para hover)
        df_scatter['caloric_label'] = df_scatter['frequent_high_caloric_food'].map({
            0: 'Não',
            1: 'Sim'
        })
        
        # Criar label para consumo de vegetais
        df_scatter['veg_label'] = df_scatter['vegetable_consumption_freq'].map({
            'rarely': 'Raramente',
            'sometimes': 'Às vezes',
            'always': 'Sempre'
        })
        
        fig_scatter = px.scatter(
            df_scatter,
            x='age_jitter',
            y='bmi_jitter',
            color='physical_activity_freq',
            color_discrete_map={
                'sedentary': '#d62728',
                'low_frequency': '#ff7f0e',
                'moderate_frequency': '#2ca02c',
                'high_frequency': '#1f77b4'
            },
            category_orders={
                'physical_activity_freq': ['sedentary', 'low_frequency', 'moderate_frequency', 'high_frequency']
            },
            labels={
                'age_jitter': 'Idade (anos)',
                'bmi_jitter': 'IMC',
                'physical_activity_freq': 'Atividade Física'
            },
            title='Distribuição de IMC por Idade e Atividade Física',
            hover_data={
                'age': True,
                'bmi': True,
                'obesity_level': True,
                'veg_label': ':.0s',
                'caloric_label': ':.0s',
                'age_jitter': False,
                'bmi_jitter': False,
                'physical_activity_freq': False
            },
            custom_data=['obesity_level', 'veg_label', 'caloric_label']
        )
        
        # Customizar hover template
        fig_scatter.update_traces(
            hovertemplate='<b>Idade:</b> %{customdata[0]}<br>' +
                          '<b>IMC:</b> %{customdata[1]}<br>' +
                          '<b>Nível Obesidade:</b> %{customdata[2]}<br>' +
                          '<b>Vegetais:</b> %{customdata[3]}<br>' +
                          '<b>Alim. Calóricos:</b> %{customdata[4]}<extra></extra>',
            marker=dict(
                size=7,
                opacity=0.35,
                line=dict(width=0, color='rgba(0,0,0,0)')
            )
        )
        
        fig_scatter.update_layout(
            height=500,
            xaxis_title='Idade (anos)',
            yaxis_title='IMC',
            legend=dict(
                title=dict(text="Atividade Física", font=dict(size=11)),
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.caption("💡 **Dica:** Cores mais intensas = maior concentração. Passe o mouse sobre os pontos para ver detalhes individuais.")
    
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
