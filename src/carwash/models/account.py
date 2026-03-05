
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Account:
    user_id: str
    login: str
    password_hash: str  # pbkdf2 hash string
    salt: str           # hex

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "login": self.login,
            "password_hash": self.password_hash,
            "salt": self.salt,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Account":
        return Account(
            user_id=d["user_id"],
            login=d["login"],
            password_hash=d["password_hash"],
            salt=d["salt"],
        )
