"""
Sistema Preditivo de Obesidade
Aplicação Streamlit para predição de níveis de obesidade usando Machine Learning

Tech Challenge - Fase 4
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import json

# Configuração da página
st.set_page_config(
    page_title="Predição de Obesidade",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2d7f3e;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .result-text {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Carregar modelo e metadados
@st.cache_resource
def load_model():
    """Carrega o modelo treinado e suas informações"""
    model_path = Path('models/obesity_risk_model_random_forest.joblib')
    info_path = Path('models/model_info.json')
    
    if not model_path.exists():
        st.error(f"❌ Modelo não encontrado em {model_path}")
        st.stop()
    
    model = joblib.load(model_path)
    
    if info_path.exists():
        with open(info_path, 'r', encoding='utf-8') as f:
            model_info = json.load(f)
    else:
        model_info = None
    
    return model, model_info

# Mapeamento de labels para português
OBESITY_LABELS = {
    'Insufficient_Weight': 'Peso Insuficiente',
    'Normal_Weight': 'Peso Normal',
    'Overweight_Level_I': 'Sobrepeso Nível I',
    'Overweight_Level_II': 'Sobrepeso Nível II',
    'Obesity_Type_I': 'Obesidade Tipo I',
    'Obesity_Type_II': 'Obesidade Tipo II',
    'Obesity_Type_III': 'Obesidade Tipo III'
}

# Descrições clínicas
OBESITY_DESCRIPTIONS = {
    'Insufficient_Weight': '⚪ Abaixo do peso ideal. Recomenda-se avaliação nutricional.',
    'Normal_Weight': '🟢 Peso saudável. Manter hábitos alimentares e atividade física.',
    'Overweight_Level_I': '🟡 Sobrepeso leve. Atenção aos hábitos alimentares e exercícios.',
    'Overweight_Level_II': '🟠 Sobrepeso moderado. Recomenda-se acompanhamento nutricional.',
    'Obesity_Type_I': '🔴 Obesidade grau I. Necessário acompanhamento médico.',
    'Obesity_Type_II': '🔴 Obesidade grau II. Requer intervenção médica urgente.',
    'Obesity_Type_III': '🔴 Obesidade grau III (mórbida). Intervenção médica imediata necessária.'
}

def calculate_bmi(weight, height):
    """Calcula o IMC"""
    return np.ceil(weight / (height ** 2))

def create_input_dataframe(data):
    """Cria DataFrame no formato esperado pelo modelo"""
    df = pd.DataFrame([data])
    
    # Calcular BMI
    df['bmi'] = calculate_bmi(df['weight'].values[0], df['height'].values[0])
    
    # Remover weight e height (não são usados no modelo)
    df = df.drop(['weight', 'height'], axis=1)
    
    return df

def main():
    # Header
    st.markdown('<div class="main-header">🏥 Sistema Preditivo de Obesidade</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Auxílio à equipe médica no diagnóstico de níveis de obesidade</div>', unsafe_allow_html=True)
    
    # Carregar modelo
    model, model_info = load_model()
    
    # Sidebar com informações do modelo
    with st.sidebar:
        st.header("ℹ️ Informações do Sistema")
        
        if model_info:
            st.metric("Modelo", "Random Forest")
            st.metric("Acurácia", f"{model_info['metrics']['accuracy']:.1%}")
            st.metric("AUC-ROC", f"{model_info['metrics']['roc_auc']:.3f}")
            
            with st.expander("📊 Métricas Detalhadas"):
                st.write(f"**Precisão:** {model_info['metrics']['precision']:.3f}")
                st.write(f"**Recall:** {model_info['metrics']['recall']:.3f}")
                st.write(f"**F1-Score:** {model_info['metrics']['f1_score']:.3f}")
                st.write(f"**Data de Treino:** {model_info['training_date']}")
        
        st.markdown("---")
        st.markdown("### 📋 Sobre o Sistema")
        st.info("""
        Este sistema utiliza Machine Learning para classificar pacientes em 7 níveis 
        de obesidade, auxiliando a equipe médica na tomada de decisão.
        
        **Categorias:**
        - Peso Insuficiente
        - Peso Normal
        - Sobrepeso (Nível I e II)
        - Obesidade (Tipo I, II e III)
        """)
    
    # Formulário de entrada
    st.header("📝 Dados do Paciente")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Informações Demográficas")
        age = st.number_input("Idade (anos)", min_value=10, max_value=100, value=25, step=1)
        gender = st.selectbox("Gênero", options=["Feminino", "Masculino"])
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01, format="%.2f")
        weight = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, format="%.1f")
        
        # Calcular e mostrar IMC
        bmi = calculate_bmi(weight, height)
        st.metric("IMC Calculado", f"{bmi:.1f}")
    
    with col2:
        st.subheader("🍽️ Hábitos Alimentares")
        main_meals = st.selectbox(
            "Refeições principais por dia",
            options=["1 refeição", "2 refeições", "3 refeições", "4 ou mais refeições"],
            index=2
        )
        vegetable_freq = st.selectbox(
            "Consumo de vegetais",
            options=["Raramente", "Às vezes", "Sempre"],
            index=1
        )
        water_intake = st.selectbox(
            "Consumo de água",
            options=["Baixo", "Adequado", "Alto"],
            index=1
        )
        high_caloric_food = st.selectbox(
            "Come alimentos altamente calóricos frequentemente?",
            options=["Não", "Sim"]
        )
        food_between_meals = st.selectbox(
            "Come entre as refeições?",
            options=["Não", "Às vezes", "Frequentemente", "Sempre"],
            index=1
        )
    
    with col3:
        st.subheader("🏃 Estilo de Vida")
        physical_activity = st.selectbox(
            "Frequência de atividade física",
            options=["Sedentário", "Baixa frequência", "Frequência moderada", "Alta frequência"],
            index=1
        )
        technology_use = st.selectbox(
            "Tempo usando tecnologia",
            options=["Baixo uso", "Uso moderado", "Alto uso"],
            index=1
        )
        smoker = st.selectbox("Fumante?", options=["Não", "Sim"])
        calorie_monitoring = st.selectbox("Monitora calorias?", options=["Não", "Sim"])
        alcohol = st.selectbox(
            "Consumo de álcool",
            options=["Não bebe", "Às vezes", "Frequentemente", "Sempre"],
            index=0
        )
        
        st.subheader("🚗 Outros")
        family_history = st.selectbox(
            "Histórico familiar de sobrepeso?",
            options=["Não", "Sim"]
        )
        transportation = st.selectbox(
            "Meio de transporte principal",
            options=["Automóvel", "Motocicleta", "Bicicleta", "Transporte Público", "A pé"],
            index=0
        )
    
    # Botão de predição
    st.markdown("---")
    if st.button("🔍 Realizar Predição", type="primary", use_container_width=True):
        
        # Preparar dados
        input_data = {
            'age': age,
            'height': height,
            'weight': weight,
            'gender': 1 if gender == "Feminino" else 0,
            'main_meals_per_day': ['one_meal', 'two_meals', 'three_meals', 'four_or_more_meals'][
                ["1 refeição", "2 refeições", "3 refeições", "4 ou mais refeições"].index(main_meals)
            ],
            'vegetable_consumption_freq': ['rarely', 'sometimes', 'always'][
                ["Raramente", "Às vezes", "Sempre"].index(vegetable_freq)
            ],
            'water_intake': ['low_consumption', 'adequate_consumption', 'high_consumption'][
                ["Baixo", "Adequado", "Alto"].index(water_intake)
            ],
            'frequent_high_caloric_food': 1 if high_caloric_food == "Sim" else 0,
            'food_between_meals': ['no', 'Sometimes', 'Frequently', 'Always'][
                ["Não", "Às vezes", "Frequentemente", "Sempre"].index(food_between_meals)
            ],
            'physical_activity_freq': ['sedentary', 'low_frequency', 'moderate_frequency', 'high_frequency'][
                ["Sedentário", "Baixa frequência", "Frequência moderada", "Alta frequência"].index(physical_activity)
            ],
            'technology_use_time': ['low_use', 'moderate_use', 'high_use'][
                ["Baixo uso", "Uso moderado", "Alto uso"].index(technology_use)
            ],
            'smoker': 1 if smoker == "Sim" else 0,
            'calorie_monitoring': 1 if calorie_monitoring == "Sim" else 0,
            'alcohol_consumption': ['no', 'Sometimes', 'Frequently', 'Always'][
                ["Não bebe", "Às vezes", "Frequentemente", "Sempre"].index(alcohol)
            ],
            'family_history_overweight': 1 if family_history == "Sim" else 0,
            'transportation_mode': ['Automobile', 'Motorbike', 'Bike', 'Public_Transportation', 'Walking'][
                ["Automóvel", "Motocicleta", "Bicicleta", "Transporte Público", "A pé"].index(transportation)
            ]
        }
        
        # Criar DataFrame
        input_df = create_input_dataframe(input_data)
        
        # Fazer predição
        with st.spinner("Analisando dados..."):
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            
            # Obter nomes das classes
            classes = model.named_steps['classifier'].classes_
        
        # Exibir resultado
        st.markdown("---")
        st.header("📊 Resultado da Análise")
        
        # Box de resultado principal
        result_label = OBESITY_LABELS.get(prediction, prediction)
        result_description = OBESITY_DESCRIPTIONS.get(prediction, "")
        
        # Determinar cor baseada no resultado
        if prediction in ['Insufficient_Weight', 'Normal_Weight']:
            result_color = "#2d7f3e"  # Verde
        elif prediction in ['Overweight_Level_I', 'Overweight_Level_II']:
            result_color = "#ff9800"  # Laranja
        else:
            result_color = "#f44336"  # Vermelho
        
        st.markdown(f"""
        <div class="prediction-box" style="border-left: 5px solid {result_color};">
            <h2 style="color: {result_color}; margin-top: 0;">Classificação: {result_label}</h2>
            <p style="font-size: 1.1rem;">{result_description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Probabilidades
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Probabilidades por Categoria")
            
            # Criar DataFrame de probabilidades
            prob_df = pd.DataFrame({
                'Categoria': [OBESITY_LABELS.get(c, c) for c in classes],
                'Probabilidade': probabilities * 100
            }).sort_values('Probabilidade', ascending=False)
            
            # Gráfico de barras
            st.bar_chart(prob_df.set_index('Categoria'))
        
        with col2:
            st.subheader("🎯 Top 3 Classificações")
            top_3 = prob_df.head(3)
            for idx, row in top_3.iterrows():
                st.metric(
                    label=row['Categoria'],
                    value=f"{row['Probabilidade']:.1f}%"
                )
        
        # Recomendações
        st.markdown("---")
        st.header("💡 Recomendações")
        
        recommendations = []
        
        if prediction in ['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']:
            recommendations.append("🔴 **Consulta médica urgente recomendada**")
            recommendations.append("📋 Avaliação completa de saúde necessária")
            recommendations.append("🥗 Acompanhamento nutricional especializado")
            recommendations.append("🏃 Programa de atividade física supervisionado")
        elif prediction in ['Overweight_Level_I', 'Overweight_Level_II']:
            recommendations.append("🟡 **Atenção aos hábitos de vida**")
            recommendations.append("🥗 Consulta com nutricionista recomendada")
            recommendations.append("🏃 Aumentar frequência de atividade física")
            recommendations.append("💧 Manter hidratação adequada")
        elif prediction == 'Normal_Weight':
            recommendations.append("🟢 **Manter hábitos saudáveis atuais**")
            recommendations.append("✅ Continue com alimentação balanceada")
            recommendations.append("✅ Mantenha atividade física regular")
            recommendations.append("✅ Realize check-ups preventivos anuais")
        else:
            recommendations.append("⚪ **Avaliação nutricional recomendada**")
            recommendations.append("🥗 Pode ser necessário aumento de ingestão calórica")
            recommendations.append("💪 Consultar sobre ganho de massa muscular")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        # Disclaimer
        st.markdown("---")
        st.warning("""
        ⚠️ **Aviso Importante:**
        Este sistema é uma ferramenta de apoio à decisão médica e não substitui a avaliação de um profissional de saúde. 
        Os resultados devem ser interpretados por médicos qualificados considerando o contexto clínico completo do paciente.
        """)

if __name__ == "__main__":
    main()
