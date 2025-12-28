# Sistema Preditivo de Obesidade

**Tech Challenge - Fase 4 | Pós Tech FIAP - Data Analytics**

Aplicação web para classificação de níveis de obesidade utilizando Machine Learning. O sistema analisa características demográficas, hábitos alimentares e estilo de vida para fornecer uma classificação precisa entre 7 níveis diferentes.

---

## Sobre o Projeto

Este projeto foi desenvolvido como parte do Tech Challenge da Pós Tech FIAP, com o objetivo de criar uma ferramenta prática para auxiliar profissionais de saúde na avaliação de risco de obesidade em pacientes.

### Níveis de Classificação

- Peso Insuficiente (Insufficient Weight)
- Peso Normal (Normal Weight)
- Sobrepeso Nível I (Overweight Level I)
- Sobrepeso Nível II (Overweight Level II)
- Obesidade Tipo I (Obesity Type I)
- Obesidade Tipo II (Obesity Type II)
- Obesidade Tipo III (Obesity Type III)

---

## Performance do Modelo

| Métrica | Valor |
|---------|-------|
| Acurácia | 93.2% |
| AUC-ROC | 0.997 |
| Precisão | 93.7% |
| Recall | 93.2% |
| F1-Score | 93.4% |

**Algoritmo:** Random Forest Classifier
**Dataset:** 2,111 registros balanceados com SMOTE

---

## Tecnologias

### Backend & ML
- Python 3.11.9
- scikit-learn 1.7.0
- pandas 2.3.3
- numpy 2.4.0
- imbalanced-learn 0.14.1
- joblib 1.5.3

### Frontend & Visualização
- Streamlit 1.52.2
- Plotly 6.5.0
- Matplotlib 3.10.8
- Seaborn 0.13.2

---

## Instalação

### Pré-requisitos
- Python 3.11+
- pip

### Setup

1. Clone o repositório
```bash
git clone https://github.com/Pedr012/TECH-CHALLENGE-FASE-4---OBESIDADE.git
cd TECH-CHALLENGE-FASE-4---OBESIDADE
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute a aplicação
```bash
streamlit run Home.py
```

Acesse em `http://localhost:8501`

---

## Uso

A aplicação possui três páginas principais:

**Home:** Visão geral do sistema e métricas do modelo

**Predição:** Insira os dados do paciente para obter uma classificação de obesidade com probabilidades e recomendações personalizadas

**Dashboard:** Explore visualizações interativas dos dados e insights sobre padrões de obesidade

---

## Metodologia

O desenvolvimento seguiu as seguintes etapas:

1. **Análise Exploratória:** Compreensão do dataset e identificação de padrões
2. **Pré-processamento:** Limpeza de dados, tratamento de valores ausentes e balanceamento com SMOTE
3. **Modelagem:** Treinamento e comparação de algoritmos (Logistic Regression vs Random Forest)
4. **Avaliação:** Validação com métricas apropriadas e análise de performance
5. **Deploy:** Desenvolvimento da interface web com Streamlit

---

## Avisos

Este sistema é uma ferramenta de apoio à decisão médica e **não substitui** a avaliação de profissionais de saúde qualificados. Todos os resultados devem ser interpretados por médicos considerando o contexto clínico completo do paciente.

---

## Deploy

### Streamlit Cloud

1. Faça push do projeto para o GitHub
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
3. Conecte seu repositório
4. Configure:
   - Main file: `Home.py`
   - Python version: 3.11
5. Deploy

### Outras Opções

- **Heroku:** Suporte a aplicações Python com Procfile
- **AWS/GCP:** Deploy em containers Docker
- **Azure:** App Service para Python

---

## Autor

**Pedro Henrique Rocha Farias**
- Tech Challenge - Pós Tech FIAP
- Fase 4: Data Visualization and Production Models

---

## Licença

MIT License - Veja o arquivo LICENSE para mais detalhes.

**Nota:** Este software é fornecido apenas para fins educacionais e de pesquisa.
