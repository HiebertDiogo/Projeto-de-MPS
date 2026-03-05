
from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional

from carwash.models.account import Account
from carwash.repositories.account_repo import AccountRepo
from carwash.services.validators import validate_login, validate_password_iam_style


class AuthService:
    
    ITERATIONS = 200_000

    def __init__(self, account_repo: AccountRepo):
        self.account_repo = account_repo

    @staticmethod
    def _pbkdf2_hash(password: str, salt_bytes: bytes, iterations: int) -> str:
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, iterations)
        return dk.hex()

    def create_account(self, user_id: str, login: str, password: str) -> tuple[bool, str]:
        ok, msg = validate_login(login)
        if not ok:
            return False, msg

        ok, msg = validate_password_iam_style(password, login)
        if not ok:
            return False, msg

        if self.account_repo.get_by_login(login) is not None:
            return False, "Esse login já existe."

        salt = secrets.token_bytes(16)
        pwd_hash = self._pbkdf2_hash(password, salt, self.ITERATIONS)

        acc = Account(
            user_id=user_id,
            login=login,
            password_hash=pwd_hash,
            salt=salt.hex(),
        )
        self.account_repo.add(acc)
        return True, "Conta criada com sucesso."

    def authenticate(self, login: str, password: str) -> tuple[bool, str, Optional[str]]:
        acc = self.account_repo.get_by_login((login or "").strip())
        if acc is None:
            return False, "Login ou senha inválidos.", None

        salt = bytes.fromhex(acc.salt)
        test_hash = self._pbkdf2_hash(password or "", salt, self.ITERATIONS)

        if not hmac.compare_digest(test_hash, acc.password_hash):
            return False, "Login ou senha inválidos.", None

        return True, "Login realizado.", acc.user_id
