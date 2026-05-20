from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
import models


class RelatorioService:
    def __init__(self, db: Session):
        self.db = db

    def obter_relatorios(self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> dict:
        # Monta os filtros dinâmicos de Data
        filtros_concluido = [models.Agendamento.status == "concluído"]
        filtros_geral = [models.Agendamento.status.in_(["concluído", "confirmado"])]

        if data_inicio:
            filtros_concluido.append(models.Agendamento.data >= data_inicio)
            filtros_geral.append(models.Agendamento.data >= data_inicio)
        if data_fim:
            filtros_concluido.append(models.Agendamento.data <= data_fim)
            filtros_geral.append(models.Agendamento.data <= data_fim)

        # FATURAMENTO
        faturamento_mes = self.db.query(func.sum(models.Servico.preco).label("total")).join(
            models.Agendamento, models.Servico.id == models.Agendamento.servico_id
        ).filter(*filtros_concluido).first()

        total_faturamento = float(faturamento_mes.total) if faturamento_mes and faturamento_mes.total else 0

        # SERVIÇOS MAIS REALIZADOS
        servicos_populares = self.db.query(
            models.Servico.id, models.Servico.nome, func.count(models.Agendamento.id).label("quantidade")
        ).join(
            models.Agendamento, models.Servico.id == models.Agendamento.servico_id
        ).filter(*filtros_concluido).group_by(models.Servico.id, models.Servico.nome).order_by(
            func.count(models.Agendamento.id).desc()
        ).limit(5).all()

        top_servicos = [
            {"id": str(s.id), "name": s.nome, "quantity": s.quantidade}
            for s in servicos_populares
        ]

        # PROFISSIONAIS MAIS AGENDADOS
        barbeiros_agendados = self.db.query(
            models.Usuario.id, models.Usuario.nome, func.count(models.Agendamento.id).label("total_agendamentos")
        ).join(
            models.Agendamento, models.Usuario.id == models.Agendamento.profissional_id
        ).filter(models.Usuario.tipo == "barber", *filtros_geral).group_by(
            models.Usuario.id, models.Usuario.nome
        ).order_by(func.count(models.Agendamento.id).desc()).limit(5).all()

        top_barbeiros = [
            {"id": str(b.id), "name": b.nome, "appointments": b.total_agendamentos}
            for b in barbeiros_agendados
        ]

        # ESTATÍSTICAS GERAIS
        total_agendamentos = self.db.query(func.count(models.Agendamento.id)).filter(*filtros_geral).scalar() or 0
        total_confirmados = self.db.query(func.count(models.Agendamento.id)).filter(
            models.Agendamento.status == "confirmado",
            *([models.Agendamento.data >= data_inicio] if data_inicio else []),
            *([models.Agendamento.data <= data_fim] if data_fim else [])
        ).scalar() or 0

        taxa_conclusao = (total_agendamentos / (total_agendamentos + total_confirmados) * 100) if total_agendamentos > 0 else 0

        return {
            "data": {
                "revenue": {"total": round(total_faturamento, 2), "currency": "BRL"},
                "topServices": top_servicos,
                "topBarbers": top_barbeiros,
                "appointments": {
                    "confirmed": total_confirmados,
                    "total": total_agendamentos,
                    "completionRate": round(taxa_conclusao, 2)
                }
            }
        }
