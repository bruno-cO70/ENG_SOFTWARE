from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.schemas.schemas import ProfissionalCreate, ProfissionalUpdate
from app.services.usuario_service import ProfissionalService
from app.repositories.repository_impl import UsuarioRepositoryImpl
import database
import models

router = APIRouter(prefix="/api/profissionais", tags=["profissionais"])


def get_profissional_service(db: Session = Depends(database.get_db)) -> ProfissionalService:
    return ProfissionalService(UsuarioRepositoryImpl(db))


def require_admin(authorization: str = None, db: Session = Depends(database.get_db)) -> models.Usuario:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    email = verify_token(authorization)
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()

    if not user or user.tipo != "barber":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem acessar este recurso.")

    return user


@router.get("")
def listar_profissionais(db: Session = Depends(database.get_db)):
    service = get_profissional_service(db)
    barbeiros = service.get_profissionais()
    return {"data": [{"id": str(b.id), "name": b.nome, "email": b.email} for b in barbeiros]}


@router.post("")
def criar_profissional(dados: ProfissionalCreate, db: Session = Depends(database.get_db),
                       current_user: models.Usuario = Depends(require_admin)):
    service = get_profissional_service(db)
    resultado = service.criar_profissional(
        nome=dados.name,
        email=dados.email,
        phone=dados.phone
    )
    return {"data": resultado}


@router.put("/{profissional_id}")
def atualizar_profissional(profissional_id: int, dados: ProfissionalUpdate,
                          db: Session = Depends(database.get_db),
                          current_user: models.Usuario = Depends(require_admin)):
    service = get_profissional_service(db)
    resultado = service.atualizar_profissional(
        profissional_id=profissional_id,
        nome=dados.name,
        email=dados.email
    )
    return {"data": resultado}


@router.delete("/{profissional_id}")
def deletar_profissional(profissional_id: int, db: Session = Depends(database.get_db),
                         current_user: models.Usuario = Depends(require_admin)):
    service = get_profissional_service(db)
    if service.deletar_profissional(profissional_id):
        return {"message": "Profissional deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Profissional não encontrado")
