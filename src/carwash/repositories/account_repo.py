
from __future__ import annotations

from typing import Optional, List
from carwash.models.account import Account
from carwash.repositories.json_db import JsonDB


class AccountRepo:
    def __init__(self, db: JsonDB):
        self.db = db

    def add(self, acc: Account) -> None:
        self.db.data["accounts"].append(acc.to_dict())
        self.db.save()

    def get_by_login(self, login: str) -> Optional[Account]:
        for a in self.db.data["accounts"]:
            if a["login"] == login:
                return Account.from_dict(a)
        return None

    def list_all(self) -> List[Account]:
        return [Account.from_dict(a) for a in self.db.data["accounts"]]
