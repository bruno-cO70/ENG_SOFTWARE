from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.interfaces.repository_interfaces import ServicoRepository, AgendamentoRepository


class ServicoService:
    def __init__(self, servico_repo: ServicoRepository):
        self.servico_repo = servico_repo

    def criar_servico(self, nome: str, preco: float, duracao_minutos: int) -> dict:
        servico = self.servico_repo.create(nome=nome, preco=preco, duracao=duracao_minutos)
        return {
            "id": str(servico.id),
            "name": servico.nome,
            "price": servico.preco
        }

    def listar_servicos(self) -> List[dict]:
        servicos = self.servico_repo.get_all()
        return [
            {
                "id": str(s.id),
                "name": s.nome,
                "durationMinutes": s.duracao,
                "price": s.preco
            }
            for s in servicos
        ]

    def atualizar_servico(self, servico_id: int, nome: str, preco: float, duracao_minutos: int) -> dict:
        servico = self.servico_repo.get_by_id(servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        servico.nome = nome
        servico.preco = preco
        servico.duracao = duracao_minutos
        servico = self.servico_repo.update(servico)

        return {
            "id": str(servico.id),
            "name": servico.nome,
            "price": servico.preco
        }

    def deletar_servico(self, servico_id: int) -> dict:
        servico = self.servico_repo.get_by_id(servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        self.servico_repo.delete(servico_id)
        return {"message": "Serviço deletado com sucesso"}


class DisponibilidadeService:
    def __init__(self, agendamento_repo: AgendamentoRepository):
        self.agendamento_repo = agendamento_repo

    def get_disponibilidade(self, profissional_id: int, data: str) -> dict:
        todos_horarios = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]

        agora = datetime.now()
        data_hoje_str = agora.strftime("%Y-%m-%d")
        hora_atual_str = agora.strftime("%H:%M")

        # Busca agendamentos ocupados para essa data e profissional
        agendamentos_ocupados = [
            a for a in self.agendamento_repo.get_all()
            if a.profissional_id == profissional_id and a.data == data and a.status != "Cancelado"
        ]
        horarios_ocupados = [a.horario for a in agendamentos_ocupados]

        slots = []
        for horario in todos_horarios:
            is_available = horario not in horarios_ocupados

            # Se estiver olhando a agenda de hoje, bloqueia horários passados
            if data == data_hoje_str and horario <= hora_atual_str:
                is_available = False

            slots.append({"time": horario, "available": is_available})

        return {"data": slots}
