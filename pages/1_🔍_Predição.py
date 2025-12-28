import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Predição de Obesidade",
    page_icon="🔍",
    layout="wide"
)

# Cache do modelo
@st.cache_resource
def load_model():
    """Carrega o modelo treinado"""
    model_path = Path("models/obesity_risk_model_random_forest.joblib")
    model = joblib.load(model_path)
    
    # Carregar informações do modelo
    info_path = Path("models/model_info.json")
    with open(info_path, 'r', encoding='utf-8') as f:
        model_info = json.load(f)
    
    return model, model_info

def calculate_bmi(weight, height):
    """Calcula o IMC"""
    return weight / (height ** 2)

def create_input_dataframe(gender, age, height, weight, family_history, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans):
    """Cria dataframe com os dados de entrada"""
    
    # Calcular IMC
    bmi = calculate_bmi(weight, height)
    
    # Mapear valores para o formato esperado pelo modelo
    # Gênero: 0 = Feminino, 1 = Masculino
    gender_val = 1 if gender == 'Masculino' else 0
    
    # Número de refeições
    meals_map = {1.0: 'one_meal', 1.5: 'one_meal', 2.0: 'two_meals', 2.5: 'two_meals', 
                 3.0: 'three_meals', 3.5: 'three_meals', 4.0: 'more_than_three'}
    main_meals = meals_map.get(ncp, 'three_meals')
    
    # Consumo de vegetais
    veg_map = {0.0: 'never', 0.5: 'never', 1.0: 'sometimes', 1.5: 'sometimes', 
               2.0: 'sometimes', 2.5: 'always', 3.0: 'always'}
    veg_consumption = veg_map.get(fcvc, 'sometimes')
    
    # Consumo de água
    water_map = {0.0: 'low_consumption', 0.5: 'low_consumption', 1.0: 'low_consumption',
                 1.5: 'adequate_consumption', 2.0: 'adequate_consumption', 2.5: 'high_consumption', 3.0: 'high_consumption'}
    water_intake = water_map.get(ch2o, 'adequate_consumption')
    
    # Comida entre refeições
    food_between_map = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}
    food_between = food_between_map.get(caec, 'Sometimes')
    
    # Atividade física
    activity_map = {0.0: 'sedentary', 0.5: 'sedentary', 1.0: 'low_frequency', 1.5: 'low_frequency',
                    2.0: 'moderate_frequency', 2.5: 'moderate_frequency', 3.0: 'high_frequency',
                    3.5: 'high_frequency', 4.0: 'high_frequency', 4.5: 'high_frequency',
                    5.0: 'high_frequency', 5.5: 'high_frequency', 6.0: 'high_frequency',
                    6.5: 'high_frequency', 7.0: 'high_frequency'}
    physical_activity = activity_map.get(faf, 'low_frequency')
    
    # Tempo de tecnologia
    tech_map = {0.0: 'low_use', 0.5: 'low_use', 1.0: 'low_use', 1.5: 'low_use',
                2.0: 'moderate_use', 2.5: 'moderate_use', 3.0: 'moderate_use', 3.5: 'moderate_use',
                4.0: 'moderate_use', 4.5: 'high_use', 5.0: 'high_use', 5.5: 'high_use',
                6.0: 'high_use', 6.5: 'high_use', 7.0: 'high_use', 7.5: 'high_use',
                8.0: 'high_use', 8.5: 'high_use', 9.0: 'high_use', 9.5: 'high_use',
                10.0: 'high_use', 10.5: 'high_use', 11.0: 'high_use', 11.5: 'high_use', 12.0: 'high_use'}
    tech_use = tech_map.get(tue, 'moderate_use')
    
    # Álcool
    alcohol_map = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}
    alcohol = alcohol_map.get(calc, 'no')
    
    # Transporte
    transport_map = {'Caminhando': 'Walking', 'Bicicleta': 'Bike', 'Motocicleta': 'Motorbike',
                     'Transporte Público': 'Public_Transportation', 'Automóvel': 'Automobile'}
    transportation = transport_map.get(mtrans, 'Public_Transportation')
    
    # Criar dicionário com as features no formato correto
    data = {
        'age': [age],
        'height': [height],
        'weight': [weight],
        'gender': [gender_val],
        'main_meals_per_day': [main_meals],
        'vegetable_consumption_freq': [veg_consumption],
        'water_intake': [water_intake],
        'frequent_high_caloric_food': [1 if favc == 'Sim' else 0],
        'food_between_meals': [food_between],
        'physical_activity_freq': [physical_activity],
        'technology_use_time': [tech_use],
        'smoker': [1 if smoke == 'Sim' else 0],
        'calorie_monitoring': [1 if scc == 'Sim' else 0],
        'alcohol_consumption': [alcohol],
        'family_history_overweight': [1 if family_history == 'Sim' else 0],
        'transportation_mode': [transportation],
        'bmi': [bmi]
    }
    
    return pd.DataFrame(data)

def main():
    st.title("🔍 Predição de Obesidade")
    st.markdown("### Diagnóstico Individual de Paciente")
    
    st.divider()
    
    # Sidebar com informações do modelo
    with st.sidebar:
        st.header("ℹ️ Informações do Modelo")
        
        try:
            model, model_info = load_model()
            
            st.metric("Acurácia", f"{model_info['metrics']['accuracy']:.1%}")
            st.metric("AUC-ROC", f"{model_info['metrics']['roc_auc']:.3f}")
            st.metric("Algoritmo", "Random Forest")
            
            st.divider()
            
            st.caption("**Classes de Obesidade:**")
            class_labels = [
                'Insufficient_Weight',
                'Normal_Weight',
                'Overweight_Level_I',
                'Overweight_Level_II',
                'Obesity_Type_I',
                'Obesity_Type_II',
                'Obesity_Type_III'
            ]
            for i, label in enumerate(class_labels, 1):
                st.caption(f"{i}. {label}")
                
        except Exception as e:
            st.error(f"Erro ao carregar modelo: {str(e)}")
            return
    
    # Formulário de entrada
    st.header("📝 Dados do Paciente")
    
    # Dados demográficos
    st.subheader("👤 Informações Demográficas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        age = st.number_input("Idade", min_value=1, max_value=120, value=25)
    
    with col2:
        height = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
    
    with col3:
        bmi = calculate_bmi(weight, height)
        st.metric("IMC Calculado", f"{bmi:.2f}")
        family_history = st.selectbox("Histórico Familiar de Sobrepeso", ["Sim", "Não"])
    
    st.divider()
    
    # Hábitos alimentares
    st.subheader("🍽️ Hábitos Alimentares")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        favc = st.selectbox("Consome alimentos calóricos frequentemente?", ["Sim", "Não"])
        fcvc = st.slider("Frequência de consumo de vegetais (0-3)", 0.0, 3.0, 2.0, 0.5)
    
    with col2:
        ncp = st.slider("Número de refeições principais (1-4)", 1.0, 4.0, 3.0, 0.5)
        caec = st.selectbox("Consumo de alimentos entre refeições", 
                           ["Não", "Às vezes", "Frequentemente", "Sempre"])
    
    with col3:
        ch2o = st.slider("Consumo diário de água (litros)", 0.0, 3.0, 2.0, 0.5)
        calc = st.selectbox("Consumo de álcool", 
                           ["Não", "Às vezes", "Frequentemente", "Sempre"])
    
    st.divider()
    
    # Estilo de vida
    st.subheader("🏃 Estilo de Vida")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        smoke = st.selectbox("Fumante?", ["Não", "Sim"])
        scc = st.selectbox("Monitora calorias?", ["Sim", "Não"])
    
    with col2:
        faf = st.slider("Frequência de atividade física (dias/semana)", 0.0, 7.0, 2.0, 0.5)
        tue = st.slider("Tempo usando dispositivos eletrônicos (horas/dia)", 0.0, 12.0, 4.0, 0.5)
    
    with col3:
        mtrans = st.selectbox("Meio de transporte principal", 
                             ["Caminhando", "Bicicleta", "Motocicleta", "Transporte Público", "Automóvel"])
    
    st.divider()
    
    # Botão de predição
    if st.button("🎯 Realizar Predição", type="primary", use_container_width=True):
        try:
            # Criar dataframe com os dados
            input_df = create_input_dataframe(
                gender, age, height, weight, family_history, favc, fcvc, ncp,
                caec, smoke, ch2o, scc, faf, tue, calc, mtrans
            )
            
            # Fazer predição
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            
            # Obter nome da classe predita
            class_labels = [
                'Insufficient_Weight',
                'Normal_Weight',
                'Overweight_Level_I',
                'Overweight_Level_II',
                'Obesity_Type_I',
                'Obesity_Type_II',
                'Obesity_Type_III'
            ]
            
            # Se prediction já é uma string, usar direto; senão, pegar do array
            if isinstance(prediction, str):
                predicted_class = prediction
                # Encontrar o índice
                prediction = class_labels.index(prediction)
            else:
                predicted_class = class_labels[int(prediction)]
            
            st.divider()
            
            # Resultado da predição
            st.header("📊 Resultado da Predição")
            
            # Definir cor baseado na classe
            if prediction <= 1:
                result_type = "success"
                icon = "✅"
            elif prediction <= 3:
                result_type = "warning"
                icon = "⚠️"
            else:
                result_type = "error"
                icon = "🚨"
            
            # Mostrar resultado
            if result_type == "success":
                st.success(f"{icon} **Classificação:** {predicted_class}")
            elif result_type == "warning":
                st.warning(f"{icon} **Classificação:** {predicted_class}")
            else:
                st.error(f"{icon} **Classificação:** {predicted_class}")
            
            st.metric("IMC", f"{bmi:.2f}")
            
            st.divider()
            
            # Probabilidades
            st.subheader("📈 Probabilidades por Classe")
            
            prob_df = pd.DataFrame({
                'Classe': class_labels,
                'Probabilidade': probabilities
            }).sort_values('Probabilidade', ascending=False)
            
            st.bar_chart(prob_df.set_index('Classe'))
            
            # Tabela de probabilidades
            prob_df['Probabilidade'] = prob_df['Probabilidade'].apply(lambda x: f"{x:.2%}")
            st.dataframe(prob_df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Recomendações
            st.subheader("💡 Recomendações")
            
            if prediction <= 1:
                st.success("""
                **Parabéns!** Você está na faixa de peso saudável.
                - Continue mantendo seus hábitos alimentares equilibrados
                - Mantenha a prática regular de atividades físicas
                - Faça check-ups médicos periódicos
                """)
            elif prediction <= 3:
                st.warning("""
                **Atenção!** Você está na faixa de sobrepeso.
                - Consulte um nutricionista para orientação alimentar
                - Aumente a frequência de atividades físicas
                - Reduza o consumo de alimentos calóricos
                - Monitore seu peso regularmente
                """)
            else:
                st.error("""
                **Importante!** Você está na faixa de obesidade.
                - **Procure orientação médica imediatamente**
                - Consulte um nutricionista especializado
                - Inicie um programa de exercícios supervisionado
                - Considere acompanhamento psicológico
                - Monitore regularmente sua saúde
                """)
            
            st.divider()
            st.caption("⚠️ **Disclaimer:** Este sistema é apenas uma ferramenta de apoio. Sempre consulte profissionais de saúde qualificados.")
            
        except Exception as e:
            st.error(f"Erro ao fazer predição: {str(e)}")

if __name__ == "__main__":
    main()
