# Guia de Migração para Nova Estrutura SOLID

## ✅ Passo 1: Estrutura Criada

A nova estrutura já foi criada em:
```
back-end/
├── app/                    # 👈 Nova estrutura aqui
│   ├── core/
│   ├── interfaces/
│   ├── repositories/
│   ├── services/
│   ├── routers/
│   ├── schemas/
│   └── main.py            # 👈 Novo ponto de entrada
│
├── models.py              # 👈 Mover para app/
├── database.py            # 👈 Mover para app/
├── email_service.py       # 👈 DELETAR (agora é app/services/email_service_impl.py)
└── main.py                # 👈 DELETAR (novo está em app/main.py)
```

---

## ✅ Passo 2: Copiar Arquivos Essenciais para app/

```bash
# Copiar models e database para app/
cp models.py app/models.py
cp database.py app/database.py
```

---

## ✅ Passo 3: Atualizar Importações

### Em `app/repositories/repository_impl.py`:
```python
# ✅ JÁ ESTÁ CORRETO:
import models
from app.interfaces.repository_interfaces import ...
```

### Em `app/routers/*.py`:
```python
# ✅ JÁ ESTÁ CORRETO:
import database
import models
from app.interfaces....
from app.repositories....
from app.services....
```

---

## ✅ Passo 4: Executar a Aplicação

### Opção 1: Executar do diretório back-end
```bash
cd c:\Users\bruno\OneDrive\Documentos\ENG_SOFTWARE\sprint_1\back-end
python -m uvicorn app.main:app --reload
```

### Opção 2: Executar do diretório app
```bash
cd c:\Users\bruno\OneDrive\Documentos\ENG_SOFTWARE\sprint_1\back-end\app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚠️ Passo 5: Verificar Variáveis de Ambiente

Certifique-se de ter `.env` configurado com:
```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hairtime

EMAIL_SENDER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
```

---

## ✅ Passo 6: Testar os Endpoints

Todos os endpoints funcionam igual ao antes:

```bash
# Registro
POST /api/auth/cadastro
{
  "name": "João",
  "email": "joao@example.com",
  "password": "senha123",
  "type": "cliente"
}

# Login
POST /api/auth/login
{
  "email": "joao@example.com",
  "password": "senha123"
}

# Criar serviço
POST /api/servicos
{
  "name": "Corte",
  "price": 50.00,
  "durationMinutes": 30
}

# Listar serviços
GET /api/servicos

# Criar agendamento
POST /api/agendamentos
{
  "barberId": "1",
  "serviceId": "1",
  "clientId": "2",
  "date": "2024-05-25",
  "time": "10:00"
}

# E todos os outros...
```

---

## 🗑️ Passo 7: Deletar Arquivos Antigos (DEPOIS DE TESTAR TUDO)

**APENAS DEPOIS DE TESTAR TUDO:**
```bash
rm main.py              # Agora está em app/main.py
rm email_service.py     # Agora está em app/services/email_service_impl.py
# Manter models.py e database.py no root ou mover para app/
```

---

## 🔍 Verificação de Funcionalidade

Rode esses testes para garantir que tudo funciona:

### 1. Teste de Autenticação
```bash
curl -X POST "http://localhost:8000/api/auth/cadastro" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"123","type":"cliente"}'
```

### 2. Teste de Serviços
```bash
curl -X GET "http://localhost:8000/api/servicos"
```

### 3. Teste de Email
```bash
curl -X POST "http://localhost:8000/api/teste-email?email_destino=seu@email.com"
```

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Linhas em main.py | ~500 | ~30 |
| Arquivos de rota | 1 | 6 |
| Serviços de negócio | Misturados | Isolados em services/ |
| Abstração de email | Nenhuma | ✅ Interface |
| Testabilidade | ❌ Difícil | ✅ Fácil |
| Manutenibilidade | ❌ Difícil | ✅ Fácil |

---

## 🚀 Próximas Melhorias (Opcionais)

1. **Adicionar testes unitários**
   ```
   tests/
   ├── test_usuario_service.py
   ├── test_agendamento_service.py
   └── test_email_service.py
   ```

2. **Adicionar logging**
   ```python
   # app/core/logger.py
   import logging
   logger = logging.getLogger(__name__)
   ```

3. **Adicionar validação customizada**
   ```python
   # app/core/validators.py
   ```

4. **Adicionar cache Redis**
   ```python
   # app/services/cache_service.py
   ```

---

## ❓ Dúvidas?

Se algo não funcionar:

1. Verifique se `.env` está configurado corretamente
2. Verifique se PostgreSQL está rodando
3. Verifique os imports em cada arquivo
4. Veja `REFACTORING_SOLID.md` para entender a arquitetura
