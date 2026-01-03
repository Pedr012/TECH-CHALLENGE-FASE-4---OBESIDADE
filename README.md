# Sistema de Análise e Predição de Obesidade

Aplicação web interativa para classificação de níveis de obesidade utilizando Machine Learning. O sistema analisa características demográficas, hábitos alimentares e estilo de vida para classificar pacientes em 7 níveis diferentes, oferecendo insights e recomendações personalizadas.

## 📋 Sobre

Sistema desenvolvido para auxiliar profissionais de saúde na avaliação de risco de obesidade. Combina análise preditiva com visualizações interativas para facilitar o entendimento de padrões e fatores de risco.

## 🎯 Funcionalidades

- **Predição Individual:** Classifique pacientes em tempo real baseado em suas características
- **Dashboard Interativo:** Visualize padrões e correlações nos dados de obesidade
- **Análise de Fatores de Risco:** Identifique combinações de fatores que influenciam a obesidade
- **Recomendações Personalizadas:** Receba sugestões baseadas no perfil do paciente
- **Métricas de Performance:** Acompanhe a acurácia e confiabilidade das predições

## 📊 Níveis de Classificação

- Peso Insuficiente
- Peso Normal
- Sobrepeso Nível I
- Sobrepeso Nível II
- Obesidade Tipo I
- Obesidade Tipo II
- Obesidade Tipo III

## ⚡ Performance do Modelo

| Métrica | Valor |
|---------|-------|
| Acurácia | 93.2% |
| AUC-ROC | 0.997 |
| Precisão | 93.7% |
| Recall | 93.2% |
| F1-Score | 93.4% |

**Algoritmo:** Random Forest Classifier  
**Dataset:** 2,111 registros balanceados

## 🛠️ Tecnologias

### Backend & Machine Learning
- Python 3.11
- scikit-learn
- pandas
- numpy
- imbalanced-learn
- joblib

### Frontend & Visualização
- Streamlit
- Plotly
- Matplotlib
- Seaborn

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11 ou superior
- pip

### Passos

**1. Clone o repositório**
```bash
git clone https://github.com/Pedr012/TECH-CHALLENGE-FASE-4---OBESIDADE.git
cd TECH-CHALLENGE-FASE-4---OBESIDADE
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a aplicação**
```bash
streamlit run Home.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📱 Como Usar

A aplicação oferece três páginas principais:

### 🏠 Home
Apresenta visão geral do sistema, métricas de performance do modelo e informações sobre as variáveis utilizadas.

### 🔍 Predição
Interface para classificação individual de pacientes:
- Insira dados demográficos (idade, altura, peso)
- Informe hábitos alimentares e estilo de vida
- Receba classificação com probabilidades
- Visualize recomendações personalizadas

### 📊 Dashboard
Explore visualizações interativas:
- Distribuição de níveis de obesidade
- Análise demográfica
- Padrões de hábitos alimentares
- Fatores de risco combinados
- Correlações entre variáveis

## 🔬 Metodologia

1. **Análise Exploratória:** Compreensão dos dados e identificação de padrões
2. **Pré-processamento:** Limpeza, tratamento de valores e balanceamento
3. **Engenharia de Features:** Criação de variáveis derivadas e transformações
4. **Modelagem:** Treinamento de algoritmos de classificação
5. **Avaliação:** Validação com métricas apropriadas
6. **Interface:** Desenvolvimento de aplicação web interativa

## ⚠️ Avisos Importantes

Este sistema é uma ferramenta de apoio à decisão e **não substitui** a avaliação de profissionais de saúde. Todos os resultados devem ser interpretados por médicos considerando o contexto clínico completo do paciente.

## 📁 Estrutura do Projeto

```
TECH-CHALLENGE-FASE-4---OBESIDADE/
├── Home.py                          # Página inicial da aplicação
├── pages/
│   ├── 1_🔍_Predição.py            # Interface de predição
│   └── 2_📊_Dashboard.py           # Visualizações e análises
├── data/
│   └── processed/
│       └── obesity_data_clean.csv  # Dados processados
├── models/
│   ├── obesity_risk_model_random_forest.joblib  # Modelo treinado
│   └── model_info.json             # Metadados do modelo
├── requirements.txt                 # Dependências Python
├── README.md                        # Documentação
└── LICENSE                          # Licença MIT
```

## 📄 Licença

MIT License - Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Nota:** Software desenvolvido para fins educacionais e de pesquisa.
