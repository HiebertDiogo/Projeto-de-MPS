from __future__ import annotations
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from carwash.services.carwash_service import CarWashService
from carwash.services.auth_service import AuthService
from carwash.repositories.factory_repo import FactoryRepo
from carwash.ui.menu import Menu

def main() -> None:
    
    carwash_service = CarWashService()
    
    account_repo = FactoryRepo.get_repository("account")
    auth_service = AuthService(account_repo, carwash_service.logger)

    Menu(carwash_service, auth_service).run()

if __name__ == "__main__":
    main()