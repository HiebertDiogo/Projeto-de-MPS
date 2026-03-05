
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from carwash.models.user import User
from carwash.models.vehicle import Vehicle
from carwash.models.service import Service
from carwash.models.service_order import ServiceOrder
from carwash.repositories.user_repo import UserRepo
from carwash.repositories.vehicle_repo import VehicleRepo
from carwash.repositories.service_repo import ServiceRepo
from carwash.repositories.order_repo import OrderRepo
from carwash.services.validators import (
    validate_non_empty,
    validate_birth_date,
    validate_email,
    validate_cpf_basic,
    clean_cpf,
    validate_plate,
)


class CarWashService:
    """Business rules (no input()) live here."""
    def __init__(self, user_repo: UserRepo, vehicle_repo: VehicleRepo, service_repo: ServiceRepo, order_repo: OrderRepo):
        self.user_repo = user_repo
        self.vehicle_repo = vehicle_repo
        self.service_repo = service_repo
        self.order_repo = order_repo

    # ---------- USERS ----------
    def register_user(self, name: str, birth_date: str, email: str, cpf: str) -> tuple[bool, str, Optional[User]]:
        if not validate_non_empty(name):
            return False, "Nome não pode ser vazio.", None
        if not validate_birth_date(birth_date):
            return False, "Data inválida. Use dd/mm/aaaa.", None
        if not validate_email(email):
            return False, "Email inválido.", None
        if not validate_cpf_basic(cpf):
            return False, "CPF inválido (precisa ter 11 dígitos).", None

        cpf_clean = clean_cpf(cpf)
        existing = self.user_repo.get_by_cpf(cpf_clean)
        if existing:
            return True, "Usuário já existia; usando o cadastro encontrado.", existing

        user = User(
            user_id=str(uuid4()),
            name=name.strip(),
            birth_date=birth_date.strip(),
            email=email.strip(),
            cpf=cpf_clean,
        )
        self.user_repo.add(user)
        return True, "Usuário cadastrado com sucesso.", user

    def list_users(self) -> List[User]:
        return self.user_repo.list_all()

    # ---------- VEHICLES ----------
    def add_vehicle(self, user_id: str, plate: str, model: str, color: str) -> tuple[bool, str]:
        if not validate_plate(plate):
            return False, "Placa inválida."
        if not validate_non_empty(model):
            return False, "Modelo não pode ser vazio."
        if not validate_non_empty(color):
            return False, "Cor não pode ser vazia."

        plate_u = plate.strip().upper()
        if self.vehicle_repo.get_by_plate(plate_u) is not None:
            return False, "Já existe um veículo cadastrado com essa placa."

        v = Vehicle(
            plate=plate_u,
            model=model.strip(),
            color=color.strip(),
            owner_user_id=user_id,
        )
        self.vehicle_repo.add(v)
        return True, "Veículo cadastrado com sucesso."

    def list_vehicles(self) -> List[Vehicle]:
        return self.vehicle_repo.list_all()

    def list_vehicles_by_user(self, user_id: str) -> List[Vehicle]:
        return self.vehicle_repo.list_by_user(user_id)

    # ---------- SERVICES (CATALOG) ----------
    def create_service(self, name: str, price_brl: float) -> tuple[bool, str, Optional[Service]]:
        if not validate_non_empty(name):
            return False, "Nome do serviço não pode ser vazio.", None
        if price_brl <= 0:
            return False, "Preço deve ser maior que zero.", None

        s = Service(
            service_id=str(uuid4()),
            name=name.strip(),
            price_brl=float(price_brl),
        )
        self.service_repo.add(s)
        return True, "Serviço cadastrado.", s

    def list_services(self) -> List[Service]:
        return self.service_repo.list_all()

    # ---------- ORDERS ----------
    def create_order(self, user_id: str, vehicle_plate: str, service_ids: List[str]) -> tuple[bool, str, Optional[ServiceOrder]]:
        if not service_ids:
            return False, "Selecione pelo menos 1 serviço.", None

        vehicle = self.vehicle_repo.get_by_plate(vehicle_plate)
        if vehicle is None:
            return False, "Veículo não encontrado.", None
        if vehicle.owner_user_id != user_id:
            return False, "Esse veículo não pertence ao usuário logado.", None

        services = []
        total = 0.0
        for sid in service_ids:
            s = self.service_repo.get_by_id(sid)
            if s is None:
                return False, f"Serviço não encontrado: {sid}", None
            services.append(s)
            total += s.price_brl

        order = ServiceOrder(
            order_id=str(uuid4()),
            user_id=user_id,
            vehicle_plate=vehicle.plate,
            service_ids=[s.service_id for s in services],
            created_at=datetime.now().isoformat(timespec="seconds"),
            total_brl=round(total, 2),
        )
        self.order_repo.add(order)
        return True, "Atendimento (ordem de serviço) criado.", order

    def list_orders(self) -> List[ServiceOrder]:
        return self.order_repo.list_all()
