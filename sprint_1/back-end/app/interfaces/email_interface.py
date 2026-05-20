from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_confirmation(self, destinatario: str, nome_cliente: str, data: str, horario: str) -> bool:
        pass

    @abstractmethod
    def send_rescheduling(self, destinatario: str, nome_cliente: str, nova_data: str, novo_horario: str) -> bool:
        pass

    @abstractmethod
    def send_test(self, destinatario: str) -> bool:
        pass
