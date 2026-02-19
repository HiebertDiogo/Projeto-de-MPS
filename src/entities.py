from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Vehicle:
    plate: str
    model: str
    color: str


@dataclass
class User:
    name: str
    birth_date: str
    email: str
    cpf: str
    vehicles: List[Vehicle] = field(default_factory=list)


@dataclass
class Manager(User):
    pass


@dataclass
class Employee(User):
    pass