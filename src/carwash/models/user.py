
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    birth_date: str  # dd/mm/yyyy
    email: str
    cpf: str         # cleaned digits only

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "birth_date": self.birth_date,
            "email": self.email,
            "cpf": self.cpf,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "User":
        return User(
            user_id=d["user_id"],
            name=d["name"],
            birth_date=d["birth_date"],
            email=d["email"],
            cpf=d["cpf"],
        )
