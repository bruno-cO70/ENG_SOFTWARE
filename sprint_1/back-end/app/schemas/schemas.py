from pydantic import BaseModel
from typing import Optional


class ServicoCreate(BaseModel):
    name: str
    price: float
    durationMinutes: int


class ServicoUpdate(BaseModel):
    name: str
    price: float
    durationMinutes: int


class AgendamentoCreate(BaseModel):
    barberId: str
    serviceId: str
    clientId: str
    date: str
    time: str


class AgendamentoUpdate(BaseModel):
    date: str
    time: str


class CadastroSchema(BaseModel):
    name: str
    email: str
    password: str
    type: str
    adminPassword: Optional[str] = None


class LoginSchema(BaseModel):
    email: str
    password: str


class ProfissionalCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ProfissionalUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
