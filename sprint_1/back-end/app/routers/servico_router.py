from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.schemas.schemas import ServicoCreate, ServicoUpdate
from app.services.servico_service import ServicoService
from app.repositories.repository_impl import ServicoRepositoryImpl
import database
import models

router = APIRouter(prefix="/api/servicos", tags=["servicos"])


def get_servico_service(db: Session = Depends(database.get_db)) -> ServicoService:
    return ServicoService(ServicoRepositoryImpl(db))


def require_admin(authorization: str = None, db: Session = Depends(database.get_db)) -> models.Usuario:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    email = verify_token(authorization)
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()

    if not user or user.tipo != "barber":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem acessar este recurso.")

    return user


@router.post("")
def criar_servico(servico: ServicoCreate, db: Session = Depends(database.get_db),
                  current_user: models.Usuario = Depends(require_admin)):
    service = get_servico_service(db)
    data = service.criar_servico(
        nome=servico.name,
        preco=servico.price,
        duracao_minutos=servico.durationMinutes
    )
    return {"data": data}


@router.get("")
def listar_servicos(db: Session = Depends(database.get_db)):
    service = get_servico_service(db)
    lista = service.listar_servicos()
    return {"data": lista}


@router.put("/{servico_id}")
def atualizar_servico(servico_id: int, servico: ServicoUpdate, db: Session = Depends(database.get_db),
                      current_user: models.Usuario = Depends(require_admin)):
    service = get_servico_service(db)
    data = service.atualizar_servico(
        servico_id=servico_id,
        nome=servico.name,
        preco=servico.price,
        duracao_minutos=servico.durationMinutes
    )
    return {"data": data}


@router.delete("/{servico_id}")
def deletar_servico(servico_id: int, db: Session = Depends(database.get_db),
                    current_user: models.Usuario = Depends(require_admin)):
    service = get_servico_service(db)
    resultado = service.deletar_servico(servico_id)
    return resultado
