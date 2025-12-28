# Guia de Deploy

Este guia apresenta opções para fazer o deploy da aplicação Streamlit em produção.

---

## Opção 1: Streamlit Cloud (Recomendado)

**Vantagens:** Gratuito, fácil, integração com GitHub, HTTPS automático

### Passo a Passo

1. **Crie uma conta em** https://streamlit.io/cloud

2. **Conecte seu repositório GitHub**
   - Faça login com GitHub
   - Autorize o Streamlit Cloud

3. **Deploy a aplicação**
   - Clique em "New app"
   - Selecione o repositório
   - Branch: `main`
   - Main file: `Home.py`
   - Clique em "Deploy"

4. **Aguarde o deploy** (2-5 minutos)

5. **Acesse sua aplicação** em `https://[seu-app].streamlit.app`

### Configurações Avançadas

Crie `.streamlit/secrets.toml` para variáveis de ambiente (se necessário):

```toml
# Não versionar este arquivo!
API_KEY = "sua-chave-aqui"
```

---

## Opção 2: Heroku

**Vantagens:** Escalável, suporte a múltiplas linguagens

### Requisitos

1. Conta no Heroku
2. Heroku CLI instalado

### Arquivos Necessários

Crie `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Crie `Procfile`:
```
web: sh setup.sh && streamlit run Home.py
```

### Deploy

```bash
# Login
heroku login

# Criar app
heroku create nome-do-app

# Deploy
git push heroku main

# Abrir app
heroku open
```

---

## Opção 3: Docker

**Vantagens:** Portabilidade, consistência entre ambientes

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
```

### Executar

```bash
# Build
docker build -t obesity-predictor .

# Run
docker run -p 8501:8501 obesity-predictor

# Ou com docker-compose
docker-compose up
```

---

## Opção 4: AWS EC2

**Vantagens:** Controle total, escalabilidade

### Setup

1. **Criar instância EC2**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Abrir porta 8501

2. **Conectar via SSH**

```bash
ssh -i key.pem ubuntu@ip-publico
```

3. **Instalar dependências**

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

4. **Clonar repositório**

```bash
git clone https://github.com/seu-usuario/repo.git
cd repo
```

5. **Configurar ambiente**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Executar com nohup**

```bash
nohup streamlit run Home.py --server.port 8501 &
```

7. **Configurar Nginx (opcional)**

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## Opção 5: Google Cloud Platform

### Cloud Run

1. **Build com Cloud Build**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/obesity-predictor
```

2. **Deploy no Cloud Run**

```bash
gcloud run deploy obesity-predictor \
  --image gcr.io/PROJECT_ID/obesity-predictor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Monitoramento

### Logs

**Streamlit Cloud:**
- Dashboard → Manage app → Logs

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker logs -f container-id
```

### Métricas

Considere adicionar:
- Google Analytics
- Sentry para error tracking
- Prometheus para métricas

---

## Segurança

### Boas Práticas

1. **Nunca versione secrets**
   - Use variáveis de ambiente
   - `.streamlit/secrets.toml` no .gitignore

2. **HTTPS**
   - Streamlit Cloud: automático
   - Heroku: automático
   - EC2: use Nginx + Let's Encrypt

3. **Rate Limiting**
   - Proteja contra abuso
   - Use proxies reversos

4. **Validação de entrada**
   - Sempre valide dados do usuário
   - Sanitize inputs

---

## Troubleshooting

### Erro de memória
- Aumente recursos da instância
- Otimize cache do Streamlit
- Reduza tamanho do modelo se possível

### Tempo limite excedido
- Configure timeout maior
- Use caching adequado
- Otimize queries/predições

### Conexão recusada
- Verifique firewall/security groups
- Confirme porta correta
- Check bind address (0.0.0.0 para externo)

---

## Custos Estimados

| Plataforma | Custo Mensal |
|------------|--------------|
| Streamlit Cloud (Community) | Grátis |
| Heroku (Hobby) | $7/mês |
| AWS EC2 (t2.micro) | Grátis (1 ano) / $8/mês |
| GCP Cloud Run | Pay-per-use (~$5-20) |
| Docker (VPS) | $5-10/mês |

---

Para mais informações, consulte a documentação oficial de cada plataforma.
