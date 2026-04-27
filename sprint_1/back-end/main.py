from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import BackgroundTasks
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext # <-- IMPORTAÇÃO DA CRIPTOGRAFIA
import models
import database
import email_service


SECRET_KEY = "chave_super_secreta_do_hairtime"
ALGORITHM = "HS256"

# ---------------------------------------------------------
# CONFIGURAÇÃO DE CRIPTOGRAFIA (Bcrypt)
# ---------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

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
    clientId: str 
    date: str
    time: str

class AgendamentoUpdate(BaseModel):
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
# ROTAS DE SERVIÇOS E AGENDAMENTOS
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

from datetime import datetime # 👈 Certifique-se de que isso está importado lá no topo!

@app.get("/api/disponibilidade")
def get_disponibilidade(profissional_id: str, data: str, db: Session = Depends(database.get_db)):
    todos_horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
    
    # Busca os ocupados
    ocupados = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == int(profissional_id),
        models.Agendamento.data == data,
        models.Agendamento.status != "Cancelado" 
    ).all()
    
    horarios_ocupados = [a.horario for a in ocupados]
    
    # 👇 NOVA LÓGICA DE TEMPO REAL
    agora = datetime.now()
    data_hoje_str = agora.strftime("%Y-%m-%d") # ex: "2024-04-10"
    hora_atual_str = agora.strftime("%H:%M")   # ex: "15:30"
    
    slots = []
    for h in todos_horarios:
        # Por padrão, está disponível se não estiver ocupado no banco
        is_available = h not in horarios_ocupados
        
        # A MÁGICA: Se o cliente estiver olhando a agenda DE HOJE...
        if data == data_hoje_str:
            # ...e a hora do botão for MENOR que a hora do relógio dele agora
            if h <= hora_atual_str:
                is_available = False # Bloqueia!
                
        slots.append({"time": h, "available": is_available})
        
    return {"data": slots}

@app.post("/api/agendamentos")
def create_agendamento(appt: AgendamentoCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    novo_agendamento = models.Agendamento(
        profissional_id=int(appt.barberId),
        cliente_id=int(appt.clientId),
        servico_id=int(appt.serviceId),
        data=appt.date,
        horario=appt.time,
        status="confirmado" 
    )
    db.add(novo_agendamento)
    db.commit()
    
    # 👇 A MÁGICA ACONTECE AQUI
    # 1. Busca os dados do cliente que acabou de agendar
    cliente = db.query(models.Usuario).filter(models.Usuario.id == int(appt.clientId)).first()
    
    if cliente:
        # 2. Usa o "BackgroundTasks" para mandar o e-mail em segundo plano. 
        # Assim o Front-end não fica travado carregando enquanto o e-mail é enviado!
        background_tasks.add_task(
            email_service.enviar_email_confirmacao, 
            destinatario=cliente.email, 
            nome_cliente=cliente.nome,
            data=appt.date, 
            horario=appt.time
        )

    return {"data": {"id": "sucesso", "status": "confirmado"}}
@app.get("/api/agendamentos")
def listar_agendamentos(db: Session = Depends(database.get_db)):
    agendamentos = db.query(models.Agendamento).all()
    lista_formatada = []
    for a in agendamentos:
        lista_formatada.append({
            "id": str(a.id),
            "date": a.data,
            "time": a.horario,
            "status": a.status,
            "clientId": str(a.cliente_id),
            "clientName": a.cliente.nome if a.cliente else "Cliente Removido",
            "barberId": str(a.profissional_id),
            "barberName": a.profissional.nome if a.profissional else "Profissional",
            "service": {"name": a.servico.nome if a.servico else "Serviço Removido"} 
        })
    return {"data": lista_formatada}

@app.patch("/api/agendamentos/{agendamento_id}/cancelar")
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(database.get_db)):
    # 1. Busca o agendamento no banco pelo ID
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    
    # 2. Valida se o agendamento existe
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    # 3. Valida se já não está cancelado (opcional, mas boa prática)
    if agendamento.status == "Cancelado":
        raise HTTPException(status_code=400, detail="Este agendamento já foi cancelado")

    # 4. Altera o status para "Cancelado"
    agendamento.status = "Cancelado"
    
    # 5. Salva a alteração no banco de dados
    db.commit()
    db.refresh(agendamento)
    
    return {"message": "Agendamento cancelado com sucesso", "status_atual": agendamento.status}

@app.put("/api/agendamentos/{agendamento_id}")
def remarcar_agendamento(agendamento_id: int, novos_dados: AgendamentoUpdate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    # 1. Busca o agendamento original
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status == "Cancelado":
        raise HTTPException(status_code=400, detail="Não é possível remarcar um agendamento cancelado")

    # 2. Validações de data no passado e conflito (mantidas iguais)
    agora = datetime.now()
    data_hoje_str = agora.strftime("%Y-%m-%d")
    hora_atual_str = agora.strftime("%H:%M")

    if novos_dados.date < data_hoje_str or (novos_dados.date == data_hoje_str and novos_dados.time <= hora_atual_str):
        raise HTTPException(status_code=400, detail="Não é possível remarcar para um horário no passado")

    conflito = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == agendamento.profissional_id,
        models.Agendamento.data == novos_dados.date,
        models.Agendamento.horario == novos_dados.time,
        models.Agendamento.status != "Cancelado",
        models.Agendamento.id != agendamento_id 
    ).first()

    if conflito:
        raise HTTPException(status_code=400, detail="Este horário já está ocupado por outro cliente")

    # 4. Aplica os novos dados e salva
    agendamento.data = novos_dados.date
    agendamento.horario = novos_dados.time
    
    db.commit()
    db.refresh(agendamento)

    # 👇 A MÁGICA DA REMARCAÇÃO AQUI
    if agendamento.cliente: # Pega os dados do cliente que já estão amarrados no agendamento
        background_tasks.add_task(
            email_service.enviar_email_remarcacao,
            destinatario=agendamento.cliente.email,
            nome_cliente=agendamento.cliente.nome,
            nova_data=agendamento.data,
            novo_horario=agendamento.horario
        )

    return {
        "message": "Agendamento remarcado com sucesso!", 
        "data": agendamento.data, 
        "time": agendamento.horario
    }

# ---------------------------------------------------------
# ROTAS DE AUTENTICAÇÃO (AGORA COM CRIPTOGRAFIA 🔒)
# ---------------------------------------------------------
@app.post("/api/auth/cadastro")
def cadastrar(usuario: CadastroSchema, db: Session = Depends(database.get_db)):
    if usuario.type == 'barber' and usuario.adminPassword != "admin123":
        raise HTTPException(status_code=403, detail="Senha master incorreta!")
    if db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

    #Aplica o Hash na senha antes de salvar no banco!
    novo_usuario = models.Usuario(
        nome=usuario.name, 
        email=usuario.email, 
        senha=get_password_hash(usuario.password), 
        tipo=usuario.type
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    token = jwt.encode({"sub": novo_usuario.email, "exp": datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"data": {"user": {"id": str(novo_usuario.id), "name": novo_usuario.nome, "email": novo_usuario.email, "type": novo_usuario.tipo}, "token": token}}

@app.post("/api/auth/login")
def login(credenciais: LoginSchema, db: Session = Depends(database.get_db)):
    #Busca apenas pelo email primeiro
    user = db.query(models.Usuario).filter(models.Usuario.email.ilike(credenciais.email)).first()
    
    #Depois verifica se o usuário existe e se a senha descriptografada bate
    if not user or not verify_password(credenciais.password, user.senha): 
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
        
    token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"data": {"user": {"id": str(user.id), "name": user.nome, "email": user.email, "type": user.tipo}, "token": token}}

# ---------------------------------------------------------
# OUTRAS ROTAS
# ---------------------------------------------------------
@app.get("/api/profissionais")
def listar_profissionais(db: Session = Depends(database.get_db)):
    barbeiros = db.query(models.Usuario).filter(models.Usuario.tipo == 'barber').all()
    return {"data": [{"id": str(b.id), "name": b.nome} for b in barbeiros]}

@app.get("/api/auth/eu")
def verificar_sessao(): return {"status": "ok"}

@app.post("/api/auth/sair")
def deslogar(): return {"message": "Sessão encerrada"}

@app.post("/api/teste-email")
def testar_envio_de_email(email_destino: str):
    sucesso = email_service.enviar_email_teste(email_destino)
    
    if sucesso:
        return {"message": f"E-mail enviado com sucesso para {email_destino}!"}
    
    raise HTTPException(status_code=500, detail="Falha ao enviar e-mail. Verifique os logs do terminal.")