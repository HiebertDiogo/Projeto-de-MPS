
from __future__ import annotations

from typing import Optional, List
from carwash.models.user import User
from carwash.repositories.json_db import JsonDB


class UserRepo:
    def __init__(self, db: JsonDB):
        self.db = db

    def add(self, user: User) -> None:
        self.db.data["users"].append(user.to_dict())
        self.db.save()

    def get_by_cpf(self, cpf: str) -> Optional[User]:
        for u in self.db.data["users"]:
            if u["cpf"] == cpf:
                return User.from_dict(u)
        return None

    def get_by_id(self, user_id: str) -> Optional[User]:
        for u in self.db.data["users"]:
            if u["user_id"] == user_id:
                return User.from_dict(u)
        return None

    def list_all(self) -> List[User]:
        return [User.from_dict(u) for u in self.db.data["users"]]

    def update(self, user: User) -> bool:
        """Atualiza os dados de um usuário existente pelo user_id. Retorna True se encontrado."""
        for idx, u in enumerate(self.db.data["users"]):
            if u["user_id"] == user.user_id:
                self.db.data["users"][idx] = user.to_dict()
                self.db.save()
                return True
        return False
