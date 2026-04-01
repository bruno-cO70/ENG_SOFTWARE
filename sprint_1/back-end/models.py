from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    tipo = Column(String)

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    duracao = Column(Integer)
    categoria = Column(String, default="hair")
    ativo = Column(Boolean, default=True)

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)
    horario = Column(String)
    
    # 👇 AS CHAVES QUE LIGAM AS TABELAS
    profissional_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    
    # 👇 RELACIONAMENTOS (Para o Python conseguir ler os nomes)
    profissional = relationship("Usuario", foreign_keys=[profissional_id])
    cliente = relationship("Usuario", foreign_keys=[cliente_id])
    servico = relationship("Servico", foreign_keys=[servico_id])