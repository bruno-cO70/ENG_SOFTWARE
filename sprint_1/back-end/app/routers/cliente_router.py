from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.services.agendamento_service import AgendamentoService
from app.repositories.repository_impl import AgendamentoRepositoryImpl, UsuarioRepositoryImpl, ServicoRepositoryImpl
from app.services.email_service_impl import EmailServiceImpl
import database

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


def get_agendamento_service(db: Session = Depends(database.get_db)) -> AgendamentoService:
    email_service = EmailServiceImpl()
    return AgendamentoService(
        AgendamentoRepositoryImpl(db),
        UsuarioRepositoryImpl(db),
        ServicoRepositoryImpl(db),
        email_service
    )


@router.get("/{cliente_id}/historico")
def obter_historico_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    service = get_agendamento_service(db)
    resultado = service.obter_historico_cliente(cliente_id)
    return resultado
