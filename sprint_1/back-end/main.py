from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

@app.get("/api/disponibilidade/{profissional_id}")
def buscar_disponibilidade(profissional_id: int, data: str, db: Session = Depends(database.get_db)):
    # Lógica simplificada para a Sprint
    todos_horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
    
    ocupados = db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == profissional_id,
        models.Agendamento.data == data
    ).all()
    
    horarios_ocupados = [a.horario for a in ocupados]
    livres = [h for h in todos_horarios if h not in horarios_ocupados]

    return {"data": data, "horarios_livres": livres}