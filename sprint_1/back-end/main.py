from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import models
import database

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
# O Front-end manda os dados em inglês (CreateAppointmentPayload), então o Pydantic tem que ler em inglês
class AgendamentoCreate(BaseModel):
    barberId: str
    serviceId: str
    date: str
    time: str
    notes: str | None = None

@app.post("/api/agendamentos")
def create_agendamento(appt: AgendamentoCreate, db: Session = Depends(database.get_db)):
    prof_id = 1 if appt.barberId == 'default' else int(appt.barberId)
    
    # Agora sim, igualzinho ao seu models.py!
    novo_agendamento = models.Agendamento(
        profissional_id=prof_id,
        data=appt.date,
        horario=appt.time
    )
    db.add(novo_agendamento)
    db.commit()
    
    return {"data": {"id": "sucesso", "status": "confirmed"}}