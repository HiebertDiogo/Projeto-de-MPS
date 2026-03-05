
from __future__ import annotations

import re
from datetime import datetime


EMAIL_RE = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PLATE_RE = re.compile(r"^[A-Z]{3}\d[A-Z0-9]\d{2}$|^[A-Z]{3}-\d{4}$")

COMMON_PASSWORDS = {
    "123456", "12345678", "password", "senha123", "qwerty", "admin123",
    "111111", "123123", "abc123", "iloveyou", "letmein", "welcome",
}


def clean_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")


def validate_cpf_basic(cpf: str) -> bool:
    """Basic CPF validation: only checks for 11 digits."""
    cpf_clean = clean_cpf(cpf)
    return len(cpf_clean) == 11


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip()))


def validate_birth_date(date_str: str) -> bool:
    """Accepts dd/mm/yyyy."""
    try:
        datetime.strptime((date_str or "").strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validate_plate(plate: str) -> bool:
    return bool(PLATE_RE.match((plate or "").strip().upper()))


def validate_non_empty(value: str) -> bool:
    return bool((value or "").strip())


def validate_login(login: str) -> tuple[bool, str]:
    """
    Requirements:
    - 12 chars
    - not empty
    - no numbers
    We'll enforce exactly 12 letters (A-Z/a-z) to avoid ambiguity.
    """
    login = (login or "").strip()
    if not login:
        return False, "Login não pode ser vazio."
    if len(login) != 12:
        return False, "Login deve ter exatamente 12 caracteres."
    if any(ch.isdigit() for ch in login):
        return False, "Login não pode conter números."
    if not login.isalpha():
        return False, "Login deve conter apenas letras (A-Z)."
    return True, ""


def validate_password_iam_style(password: str, login: str) -> tuple[bool, str]:
    """
    Simple IAM-like policy:
    - at least 10 chars
    - 1 uppercase, 1 lowercase, 1 digit, 1 special
    - cannot contain login (case-insensitive)
    - cannot be in a small common-password denylist
    """
    password = password or ""
    if len(password) < 10:
        return False, "Senha deve ter pelo menos 10 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "Senha deve conter pelo menos 1 letra maiúscula."
    if not re.search(r"[a-z]", password):
        return False, "Senha deve conter pelo menos 1 letra minúscula."
    if not re.search(r"\d", password):
        return False, "Senha deve conter pelo menos 1 número."
    if not re.search(r"[^\w\s]", password):
        return False, "Senha deve conter pelo menos 1 caractere especial (ex: !@#)."
    if login and login.lower() in password.lower():
        return False, "Senha não pode conter o login."
    if password.lower() in COMMON_PASSWORDS:
        return False, "Senha muito comum. Escolha uma senha mais forte."
    return True, ""
