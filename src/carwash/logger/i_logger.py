from __future__ import annotations

from abc import ABC, abstractmethod


class ILogger(ABC):
    """Target (GoF Adapter).

    Define o contrato que os clientes (services) utilizam.
    Os métodos têm assinatura orientada ao domínio — deliberadamente
    diferente da interface de logging.Logger (Adaptee), o que justifica
    a existência do Adapter.
    """

    @abstractmethod
    def log_info(self, message: str, context: dict) -> None:
        """Registra um evento informativo com contexto estruturado."""

    @abstractmethod
    def log_warning(self, message: str, context: dict) -> None:
        """Registra um evento de alerta com contexto estruturado."""

    @abstractmethod
    def log_error(self, message: str, context: dict) -> None:
        """Registra um evento de erro com contexto estruturado."""
