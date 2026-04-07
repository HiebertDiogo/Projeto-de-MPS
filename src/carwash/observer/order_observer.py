"""
Padrão de Projeto: Observer (GoF – Comportamental)

Define uma dependência um-para-muitos entre objetos: quando um objeto
(Subject) muda de estado, todos os seus dependentes (Observers) são
notificados automaticamente.

Aqui é usado para notificar quando uma nova Ordem de Serviço é criada.

Papéis:
  - IOrderObserver         → Observer (interface)
  - OrderEventPublisher    → Subject (publica eventos de ordem)
  - LogOrderObserver       → ConcreteObserver (loga a ordem criada)
  - SummaryOrderObserver   → ConcreteObserver (acumula estatísticas em memória)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from carwash.models.service_order import ServiceOrder


# ─── Interface Observer ───────────────────────────────────────────────────────

class IOrderObserver(ABC):
    """Interface que todos os observadores de ordens devem implementar."""

    @abstractmethod
    def on_order_created(self, order: "ServiceOrder") -> None:
        """Chamado pelo Subject quando uma nova ordem é criada."""


# ─── Subject ──────────────────────────────────────────────────────────────────

class OrderEventPublisher:
    """
    Subject: mantém lista de observers e os notifica quando uma ordem é criada.
    É instanciado como singleton dentro do CarWashService.
    """

    def __init__(self) -> None:
        self._observers: List[IOrderObserver] = []

    def subscribe(self, observer: IOrderObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: IOrderObserver) -> None:
        self._observers.remove(observer)

    def notify_order_created(self, order: "ServiceOrder") -> None:
        for obs in self._observers:
            obs.on_order_created(order)


# ─── Concrete Observers ───────────────────────────────────────────────────────

class LogOrderObserver(IOrderObserver):
    """
    ConcreteObserver: usa o logger do sistema para registrar a criação de ordens.
    """

    def __init__(self, logger) -> None:
        self._logger = logger

    def on_order_created(self, order: "ServiceOrder") -> None:
        self._logger.log_info(
            "Observer: nova ordem de serviço criada",
            {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "vehicle": order.vehicle_plate,
                "total": order.total_brl,
            },
        )


class SummaryOrderObserver(IOrderObserver):
    """
    ConcreteObserver: acumula estatísticas simples em memória
    (total de ordens e receita acumulada desde que o sistema foi iniciado).
    """

    def __init__(self) -> None:
        self.total_orders: int = 0
        self.total_revenue: float = 0.0

    def on_order_created(self, order: "ServiceOrder") -> None:
        self.total_orders += 1
        self.total_revenue += order.total_brl

    def summary(self) -> str:
        return (
            f"[Observer] Ordens na sessão: {self.total_orders} | "
            f"Receita acumulada: R$ {self.total_revenue:.2f}"
        )
