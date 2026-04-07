"""
Padrão de Projeto: Memento (GoF – Comportamental)

Permite capturar e restaurar o estado interno de um objeto (User)
sem violar o encapsulamento. Usado aqui para desfazer a última
atualização de um usuário.

Papéis:
  - UserMemento    → Memento (guarda o snapshot do User)
  - UserCaretaker  → Caretaker (armazena o último memento por user_id)
  O próprio UserRepo/CarWashService age como Originator.
"""

from __future__ import annotations
from typing import Dict, Any, Optional


class UserMemento:
    """
    Memento: guarda um snapshot imutável dos dados de um User.
    """

    def __init__(self, state: Dict[str, Any]) -> None:
        # Cópia profunda simples – todos os campos de User são primitivos
        self._state: Dict[str, Any] = dict(state)

    def get_state(self) -> Dict[str, Any]:
        return dict(self._state)

    def __repr__(self) -> str:  # pragma: no cover
        return f"UserMemento(user_id={self._state.get('user_id')!r})"


class UserCaretaker:
    """
    Caretaker: guarda o último UserMemento de cada usuário (keyed por user_id).
    Só retém um snapshot por usuário – suficiente para desfazer a última
    atualização.
    """

    def __init__(self) -> None:
        self._mementos: Dict[str, UserMemento] = {}

    def save(self, user_id: str, memento: UserMemento) -> None:
        """Salva (ou sobrescreve) o memento do usuário."""
        self._mementos[user_id] = memento

    def restore(self, user_id: str) -> Optional[UserMemento]:
        """Retorna e remove o memento, ou None se não houver snapshot."""
        return self._mementos.pop(user_id, None)

    def has_snapshot(self, user_id: str) -> bool:
        return user_id in self._mementos
