# 🚀 Guia de Deploy - Sistema Preditivo de Obesidade

## Opções de Deploy

### 1. Streamlit Cloud (Recomendado - GRATUITO)

O Streamlit Cloud é a forma mais fácil e gratuita de fazer deploy da aplicação.

#### Passo a Passo:

1. **Prepare o repositório GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Sistema Preditivo de Obesidade"
   git remote add origin <seu-repositorio-github>
   git push -u origin main
   ```

2. **Acesse Streamlit Cloud:**
   - Vá para: https://share.streamlit.io/
   - Faça login com sua conta GitHub
   - Clique em "New app"

3. **Configure o deploy:**
   - **Repository**: Selecione seu repositório
   - **Branch**: main
   - **Main file path**: `app.py`
   - Clique em "Deploy!"

4. **Aguarde o deploy:**
   - O Streamlit Cloud instalará automaticamente as dependências do `requirements.txt`
   - Em 2-5 minutos sua aplicação estará no ar
   - Você receberá uma URL como: `https://seu-usuario-sistema-obesidade.streamlit.app`

#### Vantagens:
- ✅ Totalmente gratuito
- ✅ SSL/HTTPS automático
- ✅ Atualizações automáticas com push no GitHub
- ✅ Sem necessidade de configurar servidor

---

### 2. Heroku

#### Arquivos Necessários:

**Procfile:**
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"seu-email@email.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

#### Deploy:
```bash
heroku login
heroku create nome-da-sua-app
git push heroku main
heroku open
```

---

### 3. AWS EC2 / Azure / Google Cloud

#### Para servidores VPS:

1. **Instale dependências:**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```

2. **Execute com nohup:**
   ```bash
   nohup streamlit run app.py --server.port 8501 &
   ```

3. **Configure Nginx (opcional):**
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
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

---

### 4. Docker (Para qualquer plataforma)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build e Run:**
```bash
docker build -t sistema-obesidade .
docker run -p 8501:8501 sistema-obesidade
```

**Docker Hub:**
```bash
docker tag sistema-obesidade seu-usuario/sistema-obesidade:latest
docker push seu-usuario/sistema-obesidade:latest
```

---

## 📋 Checklist Pré-Deploy

Antes de fazer deploy, verifique:

- [ ] `requirements.txt` está atualizado
- [ ] Modelo `.joblib` está na pasta `models/`
- [ ] `model_info.json` está presente
- [ ] Caminhos dos arquivos estão corretos (usar `Path` do pathlib)
- [ ] `.gitignore` está configurado
- [ ] README.md está completo
- [ ] Aplicação funciona localmente (`streamlit run app.py`)
- [ ] Sem credenciais ou senhas no código

---

## 🔗 URLs de Exemplo

Após o deploy, sua aplicação estará acessível em:

- **Streamlit Cloud**: `https://usuario-sistema-obesidade.streamlit.app`
- **Heroku**: `https://nome-app.herokuapp.com`
- **Domínio próprio**: `https://seu-dominio.com`

---

## 📊 Monitoramento

### Streamlit Cloud:
- Acesse o dashboard em https://share.streamlit.io/
- Veja logs em tempo real
- Monitore uso de recursos

### Outras plataformas:
```bash
# Ver logs
heroku logs --tail  # Heroku
docker logs container-id  # Docker

# Monitorar recursos
htop  # Linux
```

---

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError"
- Verifique se todas as dependências estão no `requirements.txt`
- Use versões específicas (ex: `pandas==2.3.3`)

### Erro: "FileNotFoundError" com modelo
- Confirme que a pasta `models/` está no repositório
- Verifique caminhos relativos no código

### App muito lento
- Adicione `@st.cache_resource` nas funções de carregamento
- Otimize o carregamento do modelo
- Use cache do Streamlit

### Erro de memória
- Streamlit Cloud tem limite de 1GB RAM
- Considere usar modelos mais leves
- Libere memória não utilizada

---

## 💡 Dicas de Otimização

1. **Cache de recursos:**
   ```python
   @st.cache_resource
   def load_model():
       return joblib.load('model.joblib')
   ```

2. **Compressão do modelo:**
   ```python
   joblib.dump(model, 'model.joblib', compress=3)
   ```

3. **Lazy loading:**
   - Carregue recursos apenas quando necessário
   - Use `st.spinner()` para feedback visual

4. **Otimização de imagens:**
   - Use formatos comprimidos (WebP, PNG otimizado)
   - Redimensione antes de exibir

---

## 📧 Suporte

Para problemas específicos:
- **Streamlit**: https://discuss.streamlit.io/
- **GitHub Issues**: Crie issue no seu repositório
- **Documentação**: https://docs.streamlit.io/

---

**Boa sorte com o deploy! 🚀**
