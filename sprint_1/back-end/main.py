from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt # <-- IMPORTANTE PARA O TOKEN
from datetime import datetime, timedelta # <-- IMPORTANTE PARA O TEMPO DO TOKEN
import models
import database

# Configurações de Segurança para o Token (JWT)
SECRET_KEY = "chave_super_secreta_do_hairtime"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. Rota de Serviços (/api/servicos)
# ---------------------------------------------------------
@app.get("/api/servicos")
def get_servicos():
    return {
        "data": [
            {"id": "1", "name": "Corte Masculino", "category": "hair", "durationMinutes": 30, "price": 35.0, "active": True},
            {"id": "2", "name": "Barba Completa", "category": "beard", "durationMinutes": 20, "price": 25.0, "active": True},
            {"id": "3", "name": "Corte + Barba", "category": "combo", "durationMinutes": 50, "price": 55.0, "active": True},
        ]
    }

# ---------------------------------------------------------
# 2. Rota de Disponibilidade (/api/disponibilidade)
# ---------------------------------------------------------
@app.get("/api/disponibilidade")
def get_disponibilidade(profissional_id: str, data: str, db: Session = Depends(database.get_db)):
    todos_horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
    
    prof_id = 1 if profissional_id == 'default' else int(profissional_id)

    ocupados = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == prof_id,
        models.Agendamento.data == data
    ).all()

    horarios_ocupados = [a.horario for a in ocupados]
    
    slots = []
    for h in todos_horarios:
        slots.append({
            "time": h,
            "available": h not in horarios_ocupados
        })

    return {"data": slots}

# ---------------------------------------------------------
# 3. Rota de Criar Agendamento (/api/agendamentos)
# ---------------------------------------------------------
class AgendamentoCreate(BaseModel):
    barberId: str
    serviceId: str
    date: str
    time: str
    notes: str | None = None

@app.post("/api/agendamentos")
def create_agendamento(appt: AgendamentoCreate, db: Session = Depends(database.get_db)):
    prof_id = 1 if appt.barberId == 'default' else int(appt.barberId)
    
    novo_agendamento = models.Agendamento(
        profissional_id=prof_id,
        data=appt.date,
        horario=appt.time
    )
    db.add(novo_agendamento)
    db.commit()
    
    return {"data": {"id": "sucesso", "status": "confirmed"}}

# ---------------------------------------------------------
# 4. Rotas de Autenticação (Cadastro e Login)
# ---------------------------------------------------------
class CadastroSchema(BaseModel):
    name: str
    email: str
    password: str
    type: str # 'client' ou 'barber'

class LoginSchema(BaseModel):
    email: str
    password: str

@app.post("/api/auth/cadastro")
def cadastrar(usuario: CadastroSchema, db: Session = Depends(database.get_db)):
    # Por enquanto é uma simulação para o Front-end conseguir logar.
    # No futuro, aqui vai o código para salvar o usuário no models.py
    
    token_data = {"sub": usuario.email, "exp": datetime.utcnow() + timedelta(days=1)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "data": {
            "user": {
                "id": "1",
                "name": usuario.name,
                "email": usuario.email,
                "type": usuario.type
            },
            "token": token
        }
    }

@app.post("/api/auth/login")
def login(credenciais: LoginSchema, db: Session = Depends(database.get_db)):
    # Simulação de login com sucesso para o Front-end
    
    token_data = {"sub": credenciais.email, "exp": datetime.utcnow() + timedelta(days=1)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "data": {
            "user": {
                "id": "1",
                "name": "Usuário Logado",
                "email": credenciais.email,
                "type": "client"
            },
            "token": token
        }
    }
# ---------------------------------------------------------
# 5. Rota para Listar Agendamentos (/api/agendamentos)
# ---------------------------------------------------------
@app.get("/api/agendamentos")
def listar_agendamentos(db: Session = Depends(database.get_db)):
    # Busca todos os agendamentos no banco SQLite
    agendamentos = db.query(models.Agendamento).all()
    
    # Formata os dados para o Vue (exatamente como o types/index.ts espera)
    lista_formatada = []
    for a in agendamentos:
        lista_formatada.append({
            "id": str(a.id),
            "date": a.data,
            "time": a.horario,
            "status": "confirmed", # Como salvamos no banco, consideramos confirmado
            "service": {"name": "Corte Masculino"} # Mock por enquanto
        })

    # O Dashboard espera os dados dentro de uma chave "data"
    return {"data": lista_formatada}