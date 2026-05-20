from typing import List, Optional
from sqlalchemy.orm import Session
from app import models
from app.interfaces.repository_interfaces import UsuarioRepository, AgendamentoRepository, ServicoRepository


class UsuarioRepositoryImpl(UsuarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str, email: str, senha: str, tipo: str) -> models.Usuario:
        usuario = models.Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_by_id(self, usuario_id: int) -> Optional[models.Usuario]:
        return self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    def get_by_email(self, email: str) -> Optional[models.Usuario]:
        return self.db.query(models.Usuario).filter(models.Usuario.email.ilike(email)).first()

    def get_all_barbers(self) -> List[models.Usuario]:
        return self.db.query(models.Usuario).filter(models.Usuario.tipo == 'barber').all()

    def update(self, usuario: models.Usuario) -> models.Usuario:
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario_id: int) -> bool:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False


class AgendamentoRepositoryImpl(AgendamentoRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_id: int, profissional_id: int, servico_id: int, data: str, horario: str, status: str) -> models.Agendamento:
        agendamento = models.Agendamento(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            servico_id=servico_id,
            data=data,
            horario=horario,
            status=status
        )
        self.db.add(agendamento)
        self.db.commit()
        self.db.refresh(agendamento)
        return agendamento

    def get_by_id(self, agendamento_id: int) -> Optional[models.Agendamento]:
        return self.db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

    def get_all(self) -> List[models.Agendamento]:
        return self.db.query(models.Agendamento).all()

    def get_by_profissional_data_hora(self, profissional_id: int, data: str, horario: str) -> Optional[models.Agendamento]:
        return self.db.query(models.Agendamento).filter(
            models.Agendamento.profissional_id == profissional_id,
            models.Agendamento.data == data,
            models.Agendamento.horario == horario,
            models.Agendamento.status != "Cancelado"
        ).first()

    def get_by_cliente(self, cliente_id: int) -> List[models.Agendamento]:
        return self.db.query(models.Agendamento).filter(models.Agendamento.cliente_id == cliente_id).all()

    def update(self, agendamento: models.Agendamento) -> models.Agendamento:
        self.db.commit()
        self.db.refresh(agendamento)
        return agendamento

    def delete(self, agendamento_id: int) -> bool:
        agendamento = self.get_by_id(agendamento_id)
        if agendamento:
            self.db.delete(agendamento)
            self.db.commit()
            return True
        return False


class ServicoRepositoryImpl(ServicoRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str, preco: float, duracao: int) -> models.Servico:
        servico = models.Servico(nome=nome, preco=preco, duracao=duracao)
        self.db.add(servico)
        self.db.commit()
        self.db.refresh(servico)
        return servico

    def get_by_id(self, servico_id: int) -> Optional[models.Servico]:
        return self.db.query(models.Servico).filter(models.Servico.id == servico_id).first()

    def get_all(self) -> List[models.Servico]:
        return self.db.query(models.Servico).all()

    def update(self, servico: models.Servico) -> models.Servico:
        self.db.commit()
        self.db.refresh(servico)
        return servico

    def delete(self, servico_id: int) -> bool:
        servico = self.get_by_id(servico_id)
        if servico:
            self.db.delete(servico)
            self.db.commit()
            return True
        return False
