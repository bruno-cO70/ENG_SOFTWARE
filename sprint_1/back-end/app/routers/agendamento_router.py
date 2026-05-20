from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.schemas.schemas import AgendamentoCreate, AgendamentoUpdate
from app.services.agendamento_service import AgendamentoService
from app.services.servico_service import DisponibilidadeService
from app.repositories.repository_impl import AgendamentoRepositoryImpl, UsuarioRepositoryImpl, ServicoRepositoryImpl
from app.services.email_service_impl import EmailServiceImpl
import database
import models

router = APIRouter(prefix="/api/agendamentos", tags=["agendamentos"])


def get_agendamento_service(db: Session = Depends(database.get_db)) -> AgendamentoService:
    email_service = EmailServiceImpl()
    return AgendamentoService(
        AgendamentoRepositoryImpl(db),
        UsuarioRepositoryImpl(db),
        ServicoRepositoryImpl(db),
        email_service
    )


def get_disponibilidade_service(db: Session = Depends(database.get_db)) -> DisponibilidadeService:
    return DisponibilidadeService(AgendamentoRepositoryImpl(db))


@router.post("")
def create_agendamento(appt: AgendamentoCreate, background_tasks: BackgroundTasks,
                       db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    resultado = service.criar_agendamento(
        cliente_id=int(appt.clientId),
        profissional_id=int(appt.barberId),
        servico_id=int(appt.serviceId),
        data=appt.date,
        horario=appt.time
    )
    return {"data": resultado}


@router.get("")
def listar_agendamentos(db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    lista = service.listar_agendamentos()
    return {"data": lista}


@router.get("/disponibilidade")
def get_disponibilidade(profissional_id: str, data: str, db: Session = Depends(database.get_db)):
    service = get_disponibilidade_service(db)
    resultado = service.get_disponibilidade(
        profissional_id=int(profissional_id),
        data=data
    )
    return resultado


@router.patch("/{agendamento_id}/cancelar")
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    resultado = service.cancelar_agendamento(agendamento_id)
    return resultado


@router.put("/{agendamento_id}")
def remarcar_agendamento(agendamento_id: int, novos_dados: AgendamentoUpdate,
                         background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    resultado = service.remarcar_agendamento(
        agendamento_id=agendamento_id,
        nova_data=novos_dados.date,
        novo_horario=novos_dados.time
    )
    return resultado
