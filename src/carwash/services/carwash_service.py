from __future__ import annotations

from typing import List, Optional

from carwash.models.user import User
from carwash.models.vehicle import Vehicle
from carwash.models.service import Service
from carwash.models.service_order import ServiceOrder

from carwash.repositories.factory_repo import FactoryRepo

from carwash.commands.base_command import Command
from carwash.commands.register_user_command import RegisterUserCommand
from carwash.services.reports.abstract_report import AbstractReport
from carwash.services.reports.html_report import HtmlReport
from carwash.services.reports.txt_report import TxtReport
from carwash.commands.add_vehicle_command import AddVehicleCommand
from carwash.commands.create_order_command import CreateOrderCommand
from carwash.commands.create_service_command import CreateServiceCommand

from carwash.services.validators import (
    validate_non_empty,
    validate_birth_date,
    validate_email,
    validate_cpf_basic,
    clean_cpf,
    validate_plate,
    clean_plate,
)

from carwash.logger.i_logger import ILogger
from carwash.logger.python_logging_adapter import build_python_logging_adapter


class CarWashService:
    """
    Business rules (Facade). 
    Esta classe centraliza o acesso a todas as funcionalidades do sistema.
    """

    def __init__(self, logger: Optional[ILogger] = None):
        """
        O __init__ agora usa a Factory para obter os repositórios,
        cumprindo o requisito de separação de camadas.
        """
      
        self.user_repo = FactoryRepo.get_repository("user")
        self.vehicle_repo = FactoryRepo.get_repository("vehicle")
        self.service_repo = FactoryRepo.get_repository("service")
        self.order_repo = FactoryRepo.get_repository("order")
        self.account_repo = FactoryRepo.get_repository("account")
        
        self.logger = logger or build_python_logging_adapter("carwash")

   # ---------- USERS ----------
    def register_user(self, name: str, birth_date: str, email: str, cpf: str) -> tuple[bool, str, Optional[User]]:
        if not validate_non_empty(name):
            return False, "Nome não pode ser vazio.", None
        if not validate_birth_date(birth_date):
            return False, "Data inválida. Use dd/mm/aaaa.", None
        if not validate_email(email):
            return False, "Email inválido.", None
        if not validate_cpf_basic(cpf):
            return False, "CPF inválido.", None

        cpf_clean = clean_cpf(cpf)
        
        existing = self.user_repo.get_by_cpf(cpf_clean)
        if existing:
            return True, "Usuário já existia.", existing

        command = RegisterUserCommand(
            user_repo=self.user_repo,
            logger=self.logger,
            name=name.strip(),
            birth_date=birth_date.strip(),
            email=email.strip(),
            cpf_clean=cpf_clean
        )
        
        user_criado = self._execute(command)
        
        return True, "Usuário cadastrado com sucesso.", user_criado

    def list_users(self) -> List[User]:
        return self.user_repo.list_all()

    # ---------- VEHICLES ----------
    
    def add_vehicle(self, user_id: str, plate: str, model: str, color: str) -> tuple[bool, str]:
    
        if not validate_plate(plate):
            self.logger.log_warning("Vehicle registration validation failed", 
                                   {"reason": "invalid plate", "value": plate, "user_id": user_id})
            return False, "Placa inválida."
        
        if not validate_non_empty(model):
            self.logger.log_warning("Vehicle registration validation failed", 
                                   {"reason": "empty model", "user_id": user_id})
            return False, "Modelo não pode ser vazio."
            
        if not validate_non_empty(color):
            self.logger.log_warning("Vehicle registration validation failed", 
                                   {"reason": "empty color", "user_id": user_id})
            return False, "Cor não pode ser vazia."

        plate_u = clean_plate(plate)
        
        if self.vehicle_repo.get_by_plate(plate_u) is not None:
            self.logger.log_warning("Vehicle plate already exists", 
                                   {"plate": plate_u, "user_id": user_id})
            return False, "Já existe um veículo cadastrado com essa placa."

        command = AddVehicleCommand(
            vehicle_repo=self.vehicle_repo,
            logger=self.logger,
            plate=plate_u,
            model=model.strip(),
            color=color.strip(),
            owner_user_id=user_id
        )
        
        self._execute(command)
        
        return True, "Veículo cadastrado com sucesso."

    def list_vehicles(self) -> List[Vehicle]:
        return self.vehicle_repo.list_all()

    def list_vehicles_by_user(self, user_id: str) -> List[Vehicle]:
        return self.vehicle_repo.list_by_user(user_id)


    # ---------- SERVICES (CATALOG) ----------
    def create_service(self, name: str, price_brl: float) -> tuple[bool, str, Optional[Service]]:
        if not validate_non_empty(name):
            self.logger.log_warning("Service creation validation failed", {"reason": "empty name"})
            return False, "Nome do serviço não pode ser vazio.", None
            
        if price_brl <= 0:
            self.logger.log_warning("Service creation validation failed", {"reason": "invalid price", "value": price_brl})
            return False, "Preço deve ser maior que zero.", None

        command = CreateServiceCommand(
            service_repo=self.service_repo,
            logger=self.logger,
            name=name.strip(),
            price_brl=price_brl
        )
        
        service = self._execute(command)
        
        return True, "Serviço cadastrado.", service

    def list_services(self) -> List[Service]:
        return self.service_repo.list_all()


    # ---------- ORDERS ----------

    def create_order(self, user_id: str, vehicle_plate: str, service_ids: List[str]) -> tuple[bool, str, Optional[ServiceOrder]]:
        #Normaliza a placa(ex: ABC-1234 vira ABC1234)
        plate_u = clean_plate(vehicle_plate)

        if not service_ids:
            self.logger.log_warning("Order failed: no services selected", {"user_id": user_id})
            return False, "Selecione pelo menos 1 serviço.", None

        vehicle = self.vehicle_repo.get_by_plate(plate_u)
        
        if vehicle is None:
            self.logger.log_warning("Order failed: vehicle not found", {"plate": plate_u})
            return False, "Veículo não encontrado.", None
            
        if vehicle.owner_user_id != user_id:
            self.logger.log_warning("Order failed: ownership mismatch", {"plate": plate_u, "user": user_id})
            return False, "Esse veículo não pertence ao usuário logado.", None

        services_found = []
        total = 0.0
        for sid in service_ids:
            s = self.service_repo.get_by_id(sid)
            if s is None:
                self.logger.log_error("Order failed: unknown service", {"service_id": sid})
                return False, f"Serviço não encontrado: {sid}", None
            services_found.append(s)
            total += s.price_brl

        command = CreateOrderCommand(
            order_repo=self.order_repo,
            logger=self.logger,
            user_id=user_id,
            vehicle_plate=vehicle.plate,
            service_ids=[s.service_id for s in services_found],
            total_brl=total
        )
        
        order = self._execute(command)
        
        return True, "Atendimento (ordem de serviço) criado.", order

    def list_orders(self) -> List[ServiceOrder]:
        return self.order_repo.list_all()

    # ---------- REPORTS ----------
    def build_report(self, fmt: str) -> AbstractReport:
        kwargs = dict(
            user_repo=self.user_repo,
            order_repo=self.order_repo,
            account_repo=self.account_repo,
            service_repo=self.service_repo,
            logger=self.logger,
        )
        fmt = fmt.strip().lower()
        if fmt == "html":
            return HtmlReport(**kwargs)
        if fmt == "txt":
            return TxtReport(**kwargs)
        raise ValueError(f"Formato de relatório desconhecido: '{fmt}'. Use 'html' ou 'txt'.")

    def _execute(self, command: Command):
        return command.execute()

    