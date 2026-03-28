from __future__ import annotations

import os

from carwash.services.reports.abstract_report import AbstractReport, ReportData


class HtmlReport(AbstractReport):
    """
    Subclasse concreta — gera relatório em formato HTML com tabelas estilizadas.
    Implementa as quatro primitivas abstratas definidas em AbstractReport.
    """

    def _format_header(self) -> str:
        return (
            "<!DOCTYPE html>\n"
            "<html lang='pt-BR'>\n"
            "<head>\n"
            "  <meta charset='UTF-8'>\n"
            "  <title>Relatório Lava Jato</title>\n"
            "  <style>\n"
            "    body { font-family: Arial, sans-serif; margin: 40px; color: #222; }\n"
            "    h1 { color: #2c3e50; }\n"
            "    h2 { color: #34495e; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 32px; }\n"
            "    table { border-collapse: collapse; width: 100%; margin-bottom: 24px; }\n"
            "    th { background-color: #2c3e50; color: white; padding: 8px 12px; text-align: left; }\n"
            "    td { padding: 7px 12px; border-bottom: 1px solid #ddd; }\n"
            "    tr:nth-child(even) { background-color: #f5f5f5; }\n"
            "    .footer { margin-top: 32px; font-size: 0.85em; color: #888; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <h1>Relatório de Estatísticas de Acesso — Lava Jato</h1>\n"
        )

    def _format_body(self, data: ReportData) -> str:
        summary_rows = (
            f"      <tr><td>Total de usuários cadastrados</td><td>{data.total_users}</td></tr>\n"
            f"      <tr><td>Usuários com conta (acessaram o sistema)</td><td>{data.total_with_accounts}</td></tr>\n"
            f"      <tr><td>Total de ordens de serviço</td><td>{data.total_orders}</td></tr>\n"
            f"      <tr><td>Receita total</td><td>R$ {data.total_revenue_brl:.2f}</td></tr>\n"
            f"      <tr><td>Gerado em</td><td>{data.generated_at}</td></tr>\n"
        )

        summary_section = (
            "  <h2>Resumo Geral</h2>\n"
            "  <table>\n"
            "    <thead><tr><th>Indicador</th><th>Valor</th></tr></thead>\n"
            "    <tbody>\n"
            f"{summary_rows}"
            "    </tbody>\n"
            "  </table>\n"
        )

        if data.per_user:
            user_rows = ""
            for rank, us in enumerate(data.per_user, start=1):
                user_rows += (
                    f"      <tr>"
                    f"<td>{rank}</td>"
                    f"<td>{us.name}</td>"
                    f"<td>{us.order_count}</td>"
                    f"<td>R$ {us.revenue_brl:.2f}</td>"
                    f"</tr>\n"
                )
        else:
            user_rows = "      <tr><td colspan='4'>Nenhuma ordem registrada.</td></tr>\n"

        ranking_section = (
            "  <h2>Ranking de Usuários por Atendimentos</h2>\n"
            "  <table>\n"
            "    <thead><tr><th>#</th><th>Usuário</th><th>Atendimentos</th><th>Receita</th></tr></thead>\n"
            "    <tbody>\n"
            f"{user_rows}"
            "    </tbody>\n"
            "  </table>\n"
        )

        return summary_section + ranking_section

    def _format_footer(self) -> str:
        return (
            "  <p class='footer'>Relatório gerado automaticamente pelo sistema Lava Jato.</p>\n"
            "</body>\n"
            "</html>\n"
        )

    def _write_output(self, path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
