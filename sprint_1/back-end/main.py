from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import models
import database


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
# SCHEMAS
# ---------------------------------------------------------
class ServicoCreate(BaseModel):
    name: str
    price: float
    durationMinutes: int

class AgendamentoCreate(BaseModel):
    barberId: str
    serviceId: str
    clientId: str # <-- Agora o Front-end avisa quem é o cliente!
    date: str
    time: str

class CadastroSchema(BaseModel):
    name: str
    email: str
    password: str
    type: str
    adminPassword: str | None = None

class LoginSchema(BaseModel):
    email: str
    password: str

# ---------------------------------------------------------
# ROTAS
# ---------------------------------------------------------
@app.post("/api/servicos")
def criar_servico(servico: ServicoCreate, db: Session = Depends(database.get_db)):
    novo_servico = models.Servico(nome=servico.name, preco=servico.price, duracao=servico.durationMinutes)
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return {"data": {"id": str(novo_servico.id), "name": novo_servico.nome, "price": novo_servico.preco}}

@app.get("/api/servicos")
def listar_servicos(db: Session = Depends(database.get_db)):
    servicos = db.query(models.Servico).all()
    lista = [{"id": str(s.id), "name": s.nome, "durationMinutes": s.duracao, "price": s.preco} for s in servicos]
    return {"data": lista}

@app.get("/api/disponibilidade")
def get_disponibilidade(profissional_id: str, data: str, db: Session = Depends(database.get_db)):
    todos_horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
    ocupados = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == int(profissional_id),
        models.Agendamento.data == data
    ).all()
    horarios_ocupados = [a.horario for a in ocupados]
    slots = [{"time": h, "available": h not in horarios_ocupados} for h in todos_horarios]
    return {"data": slots}

@app.post("/api/agendamentos")
def create_agendamento(appt: AgendamentoCreate, db: Session = Depends(database.get_db)):
    # 👇 Agora salvamos as 3 pontas da história
    novo_agendamento = models.Agendamento(
        profissional_id=int(appt.barberId),
        cliente_id=int(appt.clientId),
        servico_id=int(appt.serviceId),
        data=appt.date,
        horario=appt.time
    )
    db.add(novo_agendamento)
    db.commit()
    return {"data": {"id": "sucesso", "status": "confirmed"}}

@app.get("/api/agendamentos")
def listar_agendamentos(db: Session = Depends(database.get_db)):
    agendamentos = db.query(models.Agendamento).all()
    lista_formatada = []
    for a in agendamentos:
        # 👇 Puxamos os nomes dinamicamente!
        lista_formatada.append({
            "id": str(a.id),
            "date": a.data,
            "time": a.horario,
            "status": "confirmed",
            "clientId": str(a.cliente_id),
            "clientName": a.cliente.nome if a.cliente else "Cliente Removido",
            "barberId": str(a.profissional_id),
            "barberName": a.profissional.nome if a.profissional else "Profissional",
            "service": {"name": a.servico.nome if a.servico else "Serviço Removido"} 
        })
    return {"data": lista_formatada}

@app.post("/api/auth/cadastro")
def cadastrar(usuario: CadastroSchema, db: Session = Depends(database.get_db)):
    if usuario.type == 'barber' and usuario.adminPassword != "admin123":
        raise HTTPException(status_code=403, detail="Senha master incorreta!")
    if db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

    novo_usuario = models.Usuario(nome=usuario.name, email=usuario.email, senha=usuario.password, tipo=usuario.type)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    token = jwt.encode({"sub": novo_usuario.email, "exp": datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"data": {"user": {"id": str(novo_usuario.id), "name": novo_usuario.nome, "email": novo_usuario.email, "type": novo_usuario.tipo}, "token": token}}

@app.post("/api/auth/login")
def login(credenciais: LoginSchema, db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email.ilike(credenciais.email), models.Usuario.senha == credenciais.password).first()
    if not user: raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"data": {"user": {"id": str(user.id), "name": user.nome, "email": user.email, "type": user.tipo}, "token": token}}

@app.get("/api/profissionais")
def listar_profissionais(db: Session = Depends(database.get_db)):
    barbeiros = db.query(models.Usuario).filter(models.Usuario.tipo == 'barber').all()
    return {"data": [{"id": str(b.id), "name": b.nome} for b in barbeiros]}

@app.get("/api/auth/eu")
def verificar_sessao(): return {"status": "ok"}
@app.post("/api/auth/sair")
def deslogar(): return {"message": "Sessão encerrada"}