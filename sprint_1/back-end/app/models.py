from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "tb_usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(20), default="cliente")
    criacao = Column(DateTime, default=datetime.now)

    # Especifica que o relationship usa apenas cliente_id
    agendamentos = relationship(
        "Agendamento",
        foreign_keys="[Agendamento.cliente_id]",
        back_populates="cliente"
    )

class Servico(Base):
    
    __tablename__ = "tb_servicos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    duracao = Column(Integer, nullable=False)  
    descricao = Column(Text)

class Agendamento(Base):
    
    __tablename__ = "tb_agendamentos"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("tb_usuarios.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("tb_usuarios.id"), nullable=False) 
    servico_id = Column(Integer, ForeignKey("tb_servicos.id"), nullable=False)
    data = Column(String(10))
    horario = Column(String(5))
    status = Column(String(20), default="pendente")
    criacao = Column(DateTime, default=datetime.now)

    cliente = relationship("Usuario", foreign_keys=[cliente_id], back_populates="agendamentos")
    profissional = relationship("Usuario", foreign_keys=[profissional_id])
    servico = relationship("Servico")

class Notificacao(Base):
    
    __tablename__ = "tb_notificacoes"

    id = Column(Integer, primary_key=True)
    agendamento_id = Column(Integer, ForeignKey("tb_agendamentos.id"))
    tipo = Column(String(50), nullable=False)
    canal = Column(String(20), nullable=False)
    criacao = Column(DateTime, default=datetime.now)

    agendamento = relationship("Agendamento")

class Avaliacao(Base):

    __tablename__ = "tb_avaliacoes"

    id = Column(Integer, primary_key=True)
    agendamento_id = Column(Integer, ForeignKey("tb_agendamentos.id"), unique=True)
    nota = Column(Integer)
    comentario = Column(Text)
    criacao = Column(DateTime, default=datetime.now)

    agendamento = relationship("Agendamento")