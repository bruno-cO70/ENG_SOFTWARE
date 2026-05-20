# 🚀 Como Reativar o Servidor no Render

## ⚡ PASSO 1: Atualizar o Git

```bash
cd c:\Users\bruno\OneDrive\Documentos\ENG_SOFTWARE\sprint_1\back-end

# Adicionar os novos arquivos
git add -A

# Fazer commit
git commit -m "refactor: implementar arquitetura SOLID com camadas"

# Fazer push para o repositório remoto
git push origin main
```

---

## 🌐 PASSO 2: Configurar no Dashboard do Render

### Se estiver usando Render Web Service:

1. Acesse **https://dashboard.render.com**
2. Clique no seu serviço `hairtime-api` (ou similar)
3. Vá para **Settings**
4. Localize **Build Command** e **Start Command**
5. Atualize:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. Clique em **Save Changes**
7. Vá para **Deploy** e clique em **Manual Deploy**

---

## 🔍 PASSO 3: Verificar o Deploy

Aguarde alguns minutos e verifique:
- Status do deploy no dashboard (deve ficar verde)
- Logs: Deve aparecer `Uvicorn running on...`

---

## 📱 PASSO 4: Acessar o Swagger

Após o deploy ser bem-sucedido:

```
https://seu-app-hairtime.onrender.com/docs
```

Exemplo (substitua com sua URL real):
```
https://hairtime-api.onrender.com/docs
```

**No Swagger você consegue:**
- ✅ Ver todos os endpoints
- ✅ Testar cada rota
- ✅ Autenticar com token
- ✅ Ver exemplos de request/response

---

## 🖥️ PASSO 5: Testar Localmente (Recomendado!)

Antes de testar no Render, test localmente para garantir tudo funciona:

### 5.1 - Copiar arquivos essenciais
```bash
cd app
cp ../models.py .
cp ../database.py .
```

### 5.2 - Instalar dependências
```bash
cd ..
pip install -r requirements.txt
```

### 5.3 - Executar localmente
```bash
python -m uvicorn app.main:app --reload
```

### 5.4 - Acessar o Swagger LOCAL
```
http://localhost:8000/docs
```

---

## ✅ CHECKLIST DE TESTES

No Swagger, teste estes endpoints para garantir tudo funciona:

### 1️⃣ Autenticação
```
POST /api/auth/cadastro
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "senha123",
  "type": "cliente"
}

# Resultado esperado: Token JWT
```

### 2️⃣ Listar Serviços
```
GET /api/servicos

# Resultado esperado: Lista de serviços
```

### 3️⃣ Criar Agendamento
```
POST /api/agendamentos
{
  "barberId": "1",
  "serviceId": "1",
  "clientId": "2",
  "date": "2024-05-25",
  "time": "10:00"
}

# Resultado esperado: Agendamento criado
```

### 4️⃣ Testar Email
```
POST /api/teste-email?email_destino=seu@email.com

# Resultado esperado: Email enviado com sucesso
```

---

## 🚨 POSSÍVEIS PROBLEMAS & SOLUÇÕES

### ❌ "ModuleNotFoundError: No module named 'app'"

**Solução:** Certifique-se de que:
1. Existe o arquivo `app/__init__.py`
2. Executar do diretório correto
3. No Render, o comando está como: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

### ❌ "Error loading ASGI app"

**Solução:**
1. Verifique o Procfile (ou render.yaml)
2. Verifique se `app/main.py` existe
3. Verifique se há importações faltando em `app/main.py`

---

### ❌ "Database connection failed"

**Solução:**
1. Verifique variáveis de ambiente no Render
2. Garanta que `.env` tem as variáveis corretas:
   ```
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=localhost (ou IP do server)
   DB_PORT=5432
   DB_NAME=hairtime
   EMAIL_SENDER=seu@gmail.com
   EMAIL_PASSWORD=sua_senha_app
   ```

---

### ❌ "CORS error"

**Solução:** Já está configurado em `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 RESUMO DO FLUXO

```
1. Copiar models.py e database.py para app/
2. git add -A && git commit && git push
3. Atualizar comando no Render
4. Clicar em "Manual Deploy"
5. Esperar ~2-5 minutos
6. Acessar https://seu-app.onrender.com/docs
7. Testar no Swagger
```

---

## 🎯 DICAS IMPORTANTES

### Para Debugging:
1. Vá ao dashboard do Render
2. Clique em "Logs" para ver os erros em tempo real
3. Se der erro, corrija localmente primeiro antes de fazer push

### Para Produção:
```python
# Em app/main.py, desabilitar o host 0.0.0.0 se necessário
# Usar variáveis de ambiente para configurações sensíveis
```

### Para Escalabilidade:
- Se der erro de memória, atualize o plano do Render
- Se der timeout, aumente o timeout nas chamadas HTTP

---

## ✅ PRONTO!

Após esses passos, seu servidor estará rodando novamente com a nova arquitetura SOLID! 🚀

Qualquer dúvida, verifique os **Logs** no dashboard do Render.
