from abc import ABC, abstractmethod
from typing import List, Optional
from models import Usuario, Agendamento, Servico


class UsuarioRepository(ABC):
    @abstractmethod
    def create(self, nome: str, email: str, senha: str, tipo: str) -> Usuario:
        pass

    @abstractmethod
    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_all_barbers(self) -> List[Usuario]:
        pass

    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def delete(self, usuario_id: int) -> bool:
        pass


class AgendamentoRepository(ABC):
    @abstractmethod
    def create(self, cliente_id: int, profissional_id: int, servico_id: int, data: str, horario: str, status: str) -> Agendamento:
        pass

    @abstractmethod
    def get_by_id(self, agendamento_id: int) -> Optional[Agendamento]:
        pass

    @abstractmethod
    def get_all(self) -> List[Agendamento]:
        pass

    @abstractmethod
    def get_by_profissional_data_hora(self, profissional_id: int, data: str, horario: str) -> Optional[Agendamento]:
        pass

    @abstractmethod
    def get_by_cliente(self, cliente_id: int) -> List[Agendamento]:
        pass

    @abstractmethod
    def update(self, agendamento: Agendamento) -> Agendamento:
        pass

    @abstractmethod
    def delete(self, agendamento_id: int) -> bool:
        pass


class ServicoRepository(ABC):
    @abstractmethod
    def create(self, nome: str, preco: float, duracao: int) -> Servico:
        pass

    @abstractmethod
    def get_by_id(self, servico_id: int) -> Optional[Servico]:
        pass

    @abstractmethod
    def get_all(self) -> List[Servico]:
        pass

    @abstractmethod
    def update(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def delete(self, servico_id: int) -> bool:
        pass
