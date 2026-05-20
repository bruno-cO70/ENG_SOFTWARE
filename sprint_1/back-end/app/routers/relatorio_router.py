from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.core.security import verify_token
from app.services.relatorio_service import RelatorioService
from app import database
from app import models

router = APIRouter(prefix="/api/relatorios", tags=["relatorios"])


def get_relatorio_service(db: Session = Depends(database.get_db)) -> RelatorioService:
    return RelatorioService(db)


def require_admin(authorization: str = Header(None), db: Session = Depends(database.get_db)) -> models.Usuario:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    email = verify_token(authorization)
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()

    if not user or user.tipo != "barber":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem acessar este recurso.")

    return user


@router.get("")
def obter_relatorios(
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(require_admin)
):
    service = get_relatorio_service(db)
    resultado = service.obter_relatorios(data_inicio=data_inicio, data_fim=data_fim)
    return resultado
