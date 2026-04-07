"""
Padrão de Projeto: Strategy (GoF – Comportamental)

Define uma família de algoritmos (estratégias de desconto), encapsula
cada um e os torna intercambiáveis. Permite que o algoritmo varie
independentemente dos clientes que o usam.

Papéis:
  - IDiscountStrategy      → Strategy (interface)
  - NoDiscountStrategy     → ConcreteStrategy (sem desconto)
  - PercentDiscountStrategy→ ConcreteStrategy (desconto percentual fixo)
  - LoyaltyDiscountStrategy→ ConcreteStrategy (desconto baseado em nº de ordens)
  - DiscountContext        → Context (usado por CarWashService ao criar ordens)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from carwash.models.service_order import ServiceOrder


# ─── Interface Strategy ───────────────────────────────────────────────────────

class IDiscountStrategy(ABC):
    """Interface comum a todas as estratégias de desconto."""

    @abstractmethod
    def apply(self, base_total: float, existing_orders: List["ServiceOrder"]) -> float:
        """
        Recebe o total bruto e as ordens anteriores do usuário,
        retorna o total com desconto aplicado (>= 0).
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição curta da estratégia (exibida no menu)."""


# ─── Concrete Strategies ──────────────────────────────────────────────────────

class NoDiscountStrategy(IDiscountStrategy):
    """Sem desconto – estratégia padrão."""

    def apply(self, base_total: float, existing_orders: List["ServiceOrder"]) -> float:
        return base_total

    @property
    def description(self) -> str:
        return "Sem desconto"


class PercentDiscountStrategy(IDiscountStrategy):
    """
    Aplica um desconto percentual fixo sobre o total.
    Ex.: 10% de desconto para clientes com cupom promocional.
    """

    def __init__(self, percent: float) -> None:
        if not (0 < percent < 100):
            raise ValueError("O percentual de desconto deve estar entre 0 e 100 (exclusivo).")
        self._percent = percent

    def apply(self, base_total: float, existing_orders: List["ServiceOrder"]) -> float:
        discount = base_total * (self._percent / 100)
        return max(0.0, base_total - discount)

    @property
    def description(self) -> str:
        return f"Desconto fixo de {self._percent:.0f}%"


class LoyaltyDiscountStrategy(IDiscountStrategy):
    """
    Programa de fidelidade: o cliente ganha 15% de desconto
    a partir da 3ª ordem de serviço.
    """

    ORDERS_THRESHOLD = 3
    DISCOUNT_PERCENT = 15.0

    def apply(self, base_total: float, existing_orders: List["ServiceOrder"]) -> float:
        if len(existing_orders) >= self.ORDERS_THRESHOLD:
            discount = base_total * (self.DISCOUNT_PERCENT / 100)
            return max(0.0, base_total - discount)
        return base_total

    @property
    def description(self) -> str:
        return (
            f"Fidelidade: {self.DISCOUNT_PERCENT:.0f}% de desconto a partir "
            f"da {self.ORDERS_THRESHOLD}ª ordem"
        )


# ─── Context ──────────────────────────────────────────────────────────────────

class DiscountContext:
    """
    Context: recebe uma estratégia de desconto e a aplica ao calcular o total.
    Usado pelo CarWashService ao criar uma ordem de serviço.
    """

    def __init__(self, strategy: IDiscountStrategy | None = None) -> None:
        self._strategy: IDiscountStrategy = strategy or NoDiscountStrategy()

    @property
    def strategy(self) -> IDiscountStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: IDiscountStrategy) -> None:
        self._strategy = strategy

    def calculate_total(
        self,
        base_total: float,
        existing_orders: List["ServiceOrder"],
    ) -> float:
        return self._strategy.apply(base_total, existing_orders)
