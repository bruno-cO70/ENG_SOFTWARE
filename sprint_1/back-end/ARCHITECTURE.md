# Diagrama de Arquitetura SOLID

## 🏗️ Fluxo de Dados

```
HTTP Request (Client)
    ↓
┌─────────────────────────────┐
│  Router (Controller Layer)   │  ← Valida request, chama service
│  app/routers/               │
│  - auth_router.py           │
│  - agendamento_router.py    │
│  - servico_router.py        │
│  - profissional_router.py   │
│  - cliente_router.py        │
│  - relatorio_router.py      │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Service (Business Logic)    │  ← Regras de negócio, validações
│ app/services/               │
│ - usuario_service.py        │
│ - agendamento_service.py    │
│ - servico_service.py        │
│ - relatorio_service.py      │
│ - email_service_impl.py     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Repository (Data Access)    │  ← Acesso a dados
│ app/repositories/           │
│ - repository_impl.py        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Database (Persistence)      │  ← PostgreSQL
│ database.py                 │
│ models.py                   │
└─────────────────────────────┘
```

---

## 📦 Responsabilidade de Cada Camada

### 🚀 Router Layer (app/routers/)
- Validar entrada HTTP
- Chamar serviços
- Formatar resposta JSON
- Gerenciar autenticação/autorização

```python
@router.post("/api/agendamentos")
def create_agendamento(appt: AgendamentoCreate, db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    resultado = service.criar_agendamento(...)  # 👈 Delega para service
    return {"data": resultado}
```

---

### ⚙️ Service Layer (app/services/)
- Implementar regras de negócio
- Orquestrar repositories
- Chamar serviços externos (email, SMS)
- Lançar exceções de negócio

```python
class AgendamentoService:
    def criar_agendamento(self, cliente_id, profissional_id, ...):
        agendamento = self.agendamento_repo.create(...)  # 👈 Usa repository
        
        cliente = self.usuario_repo.get_by_id(cliente_id)
        if cliente:
            self.email_service.send_confirmation(...)  # 👈 Usa outro service
        
        return {"id": "sucesso", "status": "confirmado"}
```

---

### 💾 Repository Layer (app/repositories/)
- Abstrair acesso a banco de dados
- CRUD operations
- Queries complexas
- Nunca rejeitar com regras de negócio

```python
class AgendamentoRepositoryImpl:
    def create(self, cliente_id, profissional_id, ...):
        agendamento = models.Agendamento(...)
        self.db.add(agendamento)
        self.db.commit()  # 👈 Apenas salva, não valida
        return agendamento
```

---

### 🔌 Interface Layer (app/interfaces/)
- Contratos (ABC - Abstract Base Classes)
- Define o que cada serviço DEVE fazer
- Permite trocar implementações

```python
class EmailService(ABC):
    @abstractmethod
    def send_confirmation(self, destinatario: str, ...) -> bool:
        pass
```

---

### 🔐 Core Layer (app/core/)
- Autenticação/Autorização
- Configurações compartilhadas
- Utilities

```python
# security.py
def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(email: str) -> str:
    return jwt.encode({"sub": email}, SECRET_KEY, algorithm=ALGORITHM)
```

---

### 📋 Schemas Layer (app/schemas/)
- Validação Pydantic
- Transformação de dados
- Documentação automática (Swagger)

```python
class AgendamentoCreate(BaseModel):
    barberId: str
    serviceId: str
    clientId: str
    date: str
    time: str
```

---

## 🔄 Exemplo Completo: Criar Agendamento

```
1. Cliente faz POST /api/agendamentos
                      ↓
2. agendamento_router.create_agendamento() recebe AgendamentoCreate
                      ↓
3. Valida com Pydantic (schema)
                      ↓
4. Injeta AgendamentoService
                      ↓
5. Service.criar_agendamento():
   5a. Chama agendamento_repo.create() ← Insere no BD
   5b. Busca cliente com usuario_repo.get_by_id()
   5c. Chama email_service.send_confirmation() ← Envia email
   5d. Retorna resultado
                      ↓
6. Router formata resposta JSON
                      ↓
7. Retorna {"data": {...}} para cliente
```

---

## 🧪 Por que isso é SOLID?

### ✅ Single Responsibility
- Router apenas expõe HTTP
- Service apenas aplica lógica
- Repository apenas acessa BD
- Cada classe faz UMA coisa

### ✅ Open/Closed
- Novo tipo de email? Cria `SendGridEmailService`
- Novo banco? Cria novo repository
- Sem quebrar código existente

### ✅ Liskov Substitution
- `EmailServiceImpl` pode ser trocada por `SendGridEmailService`
- Código que usa `EmailService` não se importa qual é

### ✅ Interface Segregation
- `EmailService` tem apenas métodos de email
- Não mistura com SMS, push, etc.

### ✅ Dependency Inversion
- Service depende de `EmailService` (abstração)
- Não depende de `EmailServiceImpl` (implementação)
- Fácil fazer testes com mock

---

## 📊 Benefícios Práticos

| Cenário | Antes | Depois |
|---------|-------|--------|
| Trocar SMTP por SendGrid | Modificar 3 arquivos | 1 arquivo novo |
| Adicionar logging | Adicionar em main.py | 1 decorator em service |
| Testar agendamento | Precisa banco real | Mock de repository |
| Entender fluxo | Ler 500 linhas | Ler router → service |
| Mudar regra de negócio | Achar entre código HTTP | Está no service |

---

## 🎯 Convenções de Código

```
Router:
- request/response handling apenas
- validação de headers
- autenticação/autorização
❌ Nunca lógica de negócio

Service:
- regras de negócio
- validações complexas
- orquestração
❌ Nunca acesso direto a BD
❌ Nunca HTTP

Repository:
- CRUD simples
- queries sem regra de negócio
❌ Nunca validação
❌ Nunca chamar outro service
```

---

## 🚀 Pronto para Usar!

A arquitetura está pronta. Agora você pode:

1. ✅ Adicionar novos recursos sem quebrar código existente
2. ✅ Testar services sem banco de dados
3. ✅ Entender o fluxo rapidamente
4. ✅ Escalar para mais funcionalidades
5. ✅ Manter código limpo e organizado
