from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profissional(Base):
    __tablename__ = "profissionais"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    especialidade = Column(String)
    agendamentos = relationship("Agendamento", back_populates="profissional")

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)    # YYYY-MM-DD
    horario = Column(String) # HH:MM
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))
    profissional = relationship("Profissional", back_populates="agendamentos")