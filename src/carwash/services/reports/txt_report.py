from __future__ import annotations

import os

from carwash.services.reports.abstract_report import AbstractReport, ReportData

_WIDTH = 62  # largura total das linhas ASCII


class TxtReport(AbstractReport):
    """
    Subclasse concreta — gera relatório em texto plano com bordas ASCII.
    Implementa as quatro primitivas abstratas definidas em AbstractReport.
    """

    @staticmethod
    def _line(char: str = "-") -> str:
        return char * _WIDTH + "\n"

    def _format_header(self) -> str:
        title = "RELATORIO DE ESTATISTICAS - LAVA JATO"
        return (
            self._line("=")
            + f"{title:^{_WIDTH}}\n"
            + self._line("=")
        )

    def _format_body(self, data: ReportData) -> str:
        summary = (
            "\nRESUMO GERAL\n"
            + self._line()
            + f"  Total de usuarios cadastrados  : {data.total_users}\n"
            + f"  Usuarios com conta             : {data.total_with_accounts}\n"
            + f"  Total de ordens de servico     : {data.total_orders}\n"
            + f"  Receita total                  : R$ {data.total_revenue_brl:.2f}\n"
            + f"  Gerado em                      : {data.generated_at}\n"
            + self._line()
        )

        col_rank = 4
        col_name = 26
        col_ord = 12
        col_rev = 12

        ranking_header = (
            "\nRANKING DE USUARIOS POR ATENDIMENTOS\n"
            + self._line()
            + f"  {'#':<{col_rank}} {'Nome':<{col_name}} {'Atend.':<{col_ord}} {'Receita':>{col_rev}}\n"
            + self._line()
        )

        if data.per_user:
            ranking_rows = ""
            for rank, us in enumerate(data.per_user, start=1):
                receita = f"R$ {us.revenue_brl:.2f}"
                ranking_rows += (
                    f"  {rank:<{col_rank}} {us.name:<{col_name}} "
                    f"{us.order_count:<{col_ord}} {receita:>{col_rev}}\n"
                )
        else:
            ranking_rows = "  (Nenhuma ordem registrada)\n"

        ranking = ranking_header + ranking_rows + self._line()

        return summary + ranking

    def _format_footer(self) -> str:
        msg = "Relatorio gerado automaticamente pelo sistema Lava Jato."
        return (
            self._line("=")
            + f"  {msg}\n"
            + self._line("=")
        )

    def _write_output(self, path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
