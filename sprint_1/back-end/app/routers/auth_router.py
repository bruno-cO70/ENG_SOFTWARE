from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.schemas.schemas import CadastroSchema, LoginSchema
from app.services.usuario_service import UsuarioService
from app.repositories.repository_impl import UsuarioRepositoryImpl
from app import database

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_usuario_service(db: Session = Depends(database.get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepositoryImpl(db))


@router.post("/cadastro")
def cadastrar(usuario: CadastroSchema, db: Session = Depends(database.get_db)):
    service = get_usuario_service(db)
    data = service.registrar_usuario(
        nome=usuario.name,
        email=usuario.email,
        password=usuario.password,
        tipo=usuario.type,
        admin_password=usuario.adminPassword
    )
    return {"data": data}


@router.post("/login")
def login(credenciais: LoginSchema, db: Session = Depends(database.get_db)):
    service = get_usuario_service(db)
    data = service.login(
        email=credenciais.email,
        password=credenciais.password
    )
    return {"data": data}


@router.get("/eu")
def verificar_sessao():
    return {"status": "ok"}


@router.post("/sair")
def deslogar():
    return {"message": "Sessão encerrada"}
