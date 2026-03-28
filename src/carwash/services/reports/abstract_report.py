from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from carwash.repositories.user_repo import UserRepo
from carwash.repositories.order_repo import OrderRepo
from carwash.repositories.account_repo import AccountRepo
from carwash.repositories.service_repo import ServiceRepo
from carwash.logger.i_logger import ILogger


@dataclass
class UserStats:
    user_id: str
    name: str
    order_count: int
    revenue_brl: float


@dataclass
class ReportData:
    generated_at: str
    total_users: int
    total_with_accounts: int  # usuários que possuem Account (acessaram o sistema)
    total_orders: int
    total_revenue_brl: float
    per_user: List[UserStats] = field(default_factory=list)  # ordenado por order_count desc


class AbstractReport(ABC):
    """
    Template Method (GoF) — classe base para geração de relatórios.

    Template method  : generate()          — esqueleto do algoritmo; não sobrescrever
    Passo concreto   : _collect_data()     — invariante; coleta e agrega os dados
    Primitivas abs.  : _format_header()
                       _format_body(data)
                       _format_footer()
                       _write_output(path, content)
    """

    def __init__(
        self,
        user_repo: UserRepo,
        order_repo: OrderRepo,
        account_repo: AccountRepo,
        service_repo: ServiceRepo,
        logger: ILogger,
    ) -> None:
        self._user_repo = user_repo
        self._order_repo = order_repo
        self._account_repo = account_repo
        self._service_repo = service_repo
        self._logger = logger

    # TEMPLATE METHOD — esqueleto fixo do algoritmo

    def generate(self, output_path: str) -> str:
        """
        Gera o relatório e persiste no caminho indicado.

        Passos (ordem imutável):
          1. _collect_data()      — passo concreto, mesmo para todos os formatos
          2. _format_header()     — primitiva abstrata
          3. _format_body(data)   — primitiva abstrata
          4. _format_footer()     — primitiva abstrata
          5. _write_output(...)   — primitiva abstrata

        Retorna o caminho absoluto do arquivo gerado.
        """
        self._logger.log_info(
            "Report generation started",
            {"type": type(self).__name__, "output_path": output_path},
        )

        data: ReportData = self._collect_data()

        header: str = self._format_header()
        body: str = self._format_body(data)
        footer: str = self._format_footer()

        content: str = header + body + footer

        self._write_output(output_path, content)

        self._logger.log_info(
            "Report generation finished",
            {
                "type": type(self).__name__,
                "output_path": output_path,
                "bytes": len(content.encode()),
            },
        )
        return output_path

    # PASSO CONCRETO — invariante; subclasses não precisam (nem devem) sobrescrever

    def _collect_data(self) -> ReportData:
        """
        Consulta os repositórios e agrega as estatísticas de acesso.

        Métricas produzidas:
        - total_users            : total de usuários cadastrados
        - total_with_accounts    : usuários que possuem conta (acessaram o sistema)
        - total_orders           : total de ordens de serviço criadas
        - total_revenue_brl      : soma dos valores de todas as ordens
        - per_user               : ranking por número de atendimentos (desc)
        """
        users = self._user_repo.list_all()
        orders = self._order_repo.list_all()
        accounts = self._account_repo.list_all()

        account_user_ids = {acc.user_id for acc in accounts}
        user_map = {u.user_id: u for u in users}

        total_users = len(users)
        total_with_accounts = sum(1 for u in users if u.user_id in account_user_ids)
        total_orders = len(orders)
        total_revenue = sum(o.total_brl for o in orders)

        stats_map: dict[str, UserStats] = {}
        for order in orders:
            uid = order.user_id
            if uid not in stats_map:
                name = user_map[uid].name if uid in user_map else f"<{uid[:8]}>"
                stats_map[uid] = UserStats(
                    user_id=uid,
                    name=name,
                    order_count=0,
                    revenue_brl=0.0,
                )
            stats_map[uid].order_count += 1
            stats_map[uid].revenue_brl = round(
                stats_map[uid].revenue_brl + order.total_brl, 2
            )

        per_user = sorted(
            stats_map.values(),
            key=lambda s: (-s.order_count, -s.revenue_brl),
        )

        return ReportData(
            generated_at=datetime.now().isoformat(timespec="seconds"),
            total_users=total_users,
            total_with_accounts=total_with_accounts,
            total_orders=total_orders,
            total_revenue_brl=round(total_revenue, 2),
            per_user=per_user,
        )

    # PRIMITIVAS ABSTRATAS — cada subclasse define sua formatação

    @abstractmethod
    def _format_header(self) -> str:
        """Retorna a seção de abertura do relatório."""

    @abstractmethod
    def _format_body(self, data: ReportData) -> str:
        """Retorna o corpo do relatório com as estatísticas formatadas."""

    @abstractmethod
    def _format_footer(self) -> str:
        """Retorna a seção de fechamento do relatório."""

    @abstractmethod
    def _write_output(self, path: str, content: str) -> None:
        """Persiste o conteúdo no caminho indicado, criando diretórios se necessário."""
