from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.interfaces.repository_interfaces import AgendamentoRepository, UsuarioRepository, ServicoRepository
from app.interfaces.email_interface import EmailService


class AgendamentoService:
    def __init__(self, agendamento_repo: AgendamentoRepository, usuario_repo: UsuarioRepository,
                 servico_repo: ServicoRepository, email_service: EmailService):
        self.agendamento_repo = agendamento_repo
        self.usuario_repo = usuario_repo
        self.servico_repo = servico_repo
        self.email_service = email_service

    def criar_agendamento(self, cliente_id: int, profissional_id: int, servico_id: int, data: str, horario: str) -> dict:
        agendamento = self.agendamento_repo.create(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            servico_id=servico_id,
            data=data,
            horario=horario,
            status="confirmado"
        )

        cliente = self.usuario_repo.get_by_id(cliente_id)
        if cliente:
            self.email_service.send_confirmation(
                destinatario=cliente.email,
                nome_cliente=cliente.nome,
                data=data,
                horario=horario
            )

        return {"id": "sucesso", "status": "confirmado"}

    def listar_agendamentos(self) -> List[dict]:
        agendamentos = self.agendamento_repo.get_all()
        lista_formatada = []

        for a in agendamentos:
            lista_formatada.append({
                "id": str(a.id),
                "date": a.data,
                "time": a.horario,
                "status": a.status,
                "clientId": str(a.cliente_id),
                "clientName": a.cliente.nome if a.cliente else "Cliente Removido",
                "barberId": str(a.profissional_id),
                "barberName": a.profissional.nome if a.profissional else "Profissional",
                "service": {"name": a.servico.nome if a.servico else "Serviço Removido"}
            })

        return lista_formatada

    def cancelar_agendamento(self, agendamento_id: int) -> dict:
        agendamento = self.agendamento_repo.get_by_id(agendamento_id)

        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

        if agendamento.status == "Cancelado":
            raise HTTPException(status_code=400, detail="Este agendamento já foi cancelado")

        agendamento.status = "Cancelado"
        self.agendamento_repo.update(agendamento)

        return {"message": "Agendamento cancelado com sucesso", "status_atual": agendamento.status}

    def remarcar_agendamento(self, agendamento_id: int, nova_data: str, novo_horario: str) -> dict:
        agendamento = self.agendamento_repo.get_by_id(agendamento_id)

        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

        if agendamento.status == "Cancelado":
            raise HTTPException(status_code=400, detail="Não é possível remarcar um agendamento cancelado")

        agora = datetime.now()
        data_hoje_str = agora.strftime("%Y-%m-%d")
        hora_atual_str = agora.strftime("%H:%M")

        if nova_data < data_hoje_str or (nova_data == data_hoje_str and novo_horario <= hora_atual_str):
            raise HTTPException(status_code=400, detail="Não é possível remarcar para um horário no passado")

        conflito = self.agendamento_repo.get_by_profissional_data_hora(
            agendamento.profissional_id,
            nova_data,
            novo_horario
        )

        if conflito and conflito.id != agendamento_id:
            raise HTTPException(status_code=400, detail="Este horário já está ocupado por outro cliente")

        agendamento.data = nova_data
        agendamento.horario = novo_horario
        self.agendamento_repo.update(agendamento)

        if agendamento.cliente:
            self.email_service.send_rescheduling(
                destinatario=agendamento.cliente.email,
                nome_cliente=agendamento.cliente.nome,
                nova_data=nova_data,
                novo_horario=novo_horario
            )

        return {
            "message": "Agendamento remarcado com sucesso!",
            "data": agendamento.data,
            "time": agendamento.horario
        }

    def obter_historico_cliente(self, cliente_id: int) -> dict:
        cliente = self.usuario_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        agora = datetime.now()
        data_hoje_str = agora.strftime("%Y-%m-%d")

        agendamentos_historico = [
            a for a in self.agendamento_repo.get_by_cliente(cliente_id)
            if a.data < data_hoje_str and a.status in ["concluído", "Cancelado"]
        ]

        lista_formatada = []
        for a in agendamentos_historico:
            lista_formatada.append({
                "id": str(a.id),
                "date": a.data,
                "time": a.horario,
                "status": a.status,
                "barberId": str(a.profissional_id),
                "barberName": a.profissional.nome if a.profissional else "Profissional Removido",
                "service": {
                    "name": a.servico.nome if a.servico else "Serviço Removido",
                    "price": float(a.servico.preco) if a.servico else 0
                },
                "createdAt": a.criacao.isoformat() if a.criacao else None
            })

        return {
            "data": lista_formatada,
            "total": len(lista_formatada),
            "clientId": str(cliente_id),
            "clientName": cliente.nome
        }
