# Comandos Git para Publicação

## Primeira Vez - Inicializar Repositório

### 1. Inicializar Git
```bash
git init
```

### 2. Adicionar todos os arquivos
```bash
git add .
```

### 3. Primeiro commit
```bash
git commit -m "Initial commit: Sistema Preditivo de Obesidade"
```

### 4. Criar repositório no GitHub
- Acesse https://github.com/new
- Nome: `tech-challenge-obesidade` (ou outro nome)
- Descrição: "Sistema de ML para classificação de níveis de obesidade - Tech Challenge Fase 4"
- Público ou Privado (conforme preferência)
- NÃO marque "Initialize with README" (já temos)
- Clique em "Create repository"

### 5. Conectar ao repositório remoto
```bash
git remote add origin https://github.com/SEU-USUARIO/tech-challenge-obesidade.git
```

### 6. Enviar código
```bash
git branch -M main
git push -u origin main
```

---

## Atualizações Futuras

### Verificar status
```bash
git status
```

### Adicionar mudanças
```bash
# Todos os arquivos
git add .

# Ou arquivos específicos
git add arquivo.py
```

### Commit
```bash
git commit -m "Descrição clara da mudança"
```

### Enviar para GitHub
```bash
git push
```

---

## Comandos Úteis

### Ver histórico
```bash
git log --oneline
```

### Criar nova branch
```bash
git checkout -b feature/nova-funcionalidade
```

### Voltar para main
```bash
git checkout main
```

### Merge de branch
```bash
git checkout main
git merge feature/nova-funcionalidade
```

### Desfazer último commit (mantém alterações)
```bash
git reset --soft HEAD~1
```

### Atualizar do repositório remoto
```bash
git pull
```

### Ver diferenças
```bash
git diff
```

---

## Estrutura de Commits (Boa Prática)

Use mensagens claras e descritivas:

```bash
# Exemplos
git commit -m "feat: Adiciona filtro de idade no dashboard"
git commit -m "fix: Corrige erro de predição com valores nulos"
git commit -m "docs: Atualiza README com instruções de deploy"
git commit -m "refactor: Melhora performance do modelo"
git commit -m "style: Ajusta tema dark do Streamlit"
```

Prefixos comuns:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, estilo
- `refactor`: Refatoração de código
- `test`: Testes
- `chore`: Manutenção, configs

---

## Verificação Antes de Publicar

### Checklist

- [ ] Código testado e funcionando
- [ ] README.md atualizado
- [ ] requirements.txt atualizado
- [ ] Sem credenciais/secrets no código
- [ ] .gitignore configurado corretamente
- [ ] Comentários desnecessários removidos
- [ ] Arquivos temporários não incluídos

### Arquivos que NÃO devem ser versionados

Já configurados no `.gitignore`:
- `TechFase4/` (ambiente virtual)
- `__pycache__/`
- `.vscode/`
- `.streamlit/secrets.toml`
- Arquivos temporários

---

## Problemas Comuns

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin URL-DO-SEU-REPO
```

### "failed to push some refs"
```bash
git pull --rebase origin main
git push
```

### Remover arquivo já commitado
```bash
git rm --cached arquivo.py
# Adicione ao .gitignore
git commit -m "Remove arquivo do versionamento"
git push
```

---

## Próximos Passos Após Publicar

1. **Adicionar badges ao README** (opcional)
   - Build status
   - License
   - Python version

2. **Configurar GitHub Pages** (se aplicável)
   - Para documentação adicional

3. **Criar Releases**
   - Tag versões importantes
   - Changelog de mudanças

4. **Issues e Projects**
   - Organize melhorias futuras
   - Track bugs

---

## Exemplo Completo

```bash
# 1. Verificar status
git status

# 2. Adicionar mudanças
git add .

# 3. Commit descritivo
git commit -m "feat: Adiciona sistema completo de predição de obesidade"

# 4. Primeira vez: conectar remote
git remote add origin https://github.com/SEU-USUARIO/tech-challenge-obesidade.git

# 5. Push
git branch -M main
git push -u origin main

# 6. Após primeira vez, apenas:
git push
```

---

**Pronto!** Seu projeto estará publicado no GitHub e pronto para deploy no Streamlit Cloud.
