from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.interfaces.repository_interfaces import UsuarioRepository, AgendamentoRepository, ServicoRepository
from app.interfaces.email_interface import EmailService
from app.core.security import verify_password, get_password_hash, create_access_token


class UsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def registrar_usuario(self, nome: str, email: str, password: str, tipo: str, admin_password: Optional[str] = None) -> dict:
        if tipo == 'barber' and admin_password != "admin123":
            raise HTTPException(status_code=403, detail="Senha master incorreta!")

        if self.usuario_repo.get_by_email(email):
            raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

        usuario = self.usuario_repo.create(
            nome=nome,
            email=email,
            senha=get_password_hash(password),
            tipo=tipo
        )

        token = create_access_token(usuario.email)
        return {
            "user": {
                "id": str(usuario.id),
                "name": usuario.nome,
                "email": usuario.email,
                "type": usuario.tipo
            },
            "token": token
        }

    def login(self, email: str, password: str) -> dict:
        usuario = self.usuario_repo.get_by_email(email)

        if not usuario or not verify_password(password, usuario.senha):
            raise HTTPException(status_code=401, detail="Email ou senha incorretos")

        token = create_access_token(usuario.email)
        return {
            "user": {
                "id": str(usuario.id),
                "name": usuario.nome,
                "email": usuario.email,
                "type": usuario.tipo
            },
            "token": token
        }

    def get_usuario(self, usuario_id: int):
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario

    def get_profissionais(self):
        return self.usuario_repo.get_all_barbers()


class ProfissionalService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def get_profissionais(self):
        # O Service pede para o Repository buscar os barbeiros no banco
        return self.usuario_repo.get_all_barbers()

    def criar_profissional(self, nome: str, email: str, phone: Optional[str] = None) -> dict:
        profissional = self.usuario_repo.create(
            nome=nome,
            email=email,
            senha=get_password_hash(email),
            tipo='barber'
        )
        return {
            "id": str(profissional.id),
            "name": profissional.nome,
            "email": profissional.email
        }

    def atualizar_profissional(self, profissional_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> dict:
        profissional = self.usuario_repo.get_by_id(profissional_id)
        if not profissional:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")

        if nome:
            profissional.nome = nome
        if email:
            profissional.email = email

        profissional = self.usuario_repo.update(profissional)
        return {
            "id": str(profissional.id),
            "name": profissional.nome,
            "email": profissional.email
        }

    def deletar_profissional(self, profissional_id: int) -> bool:
        return self.usuario_repo.delete(profissional_id)
