
from __future__ import annotations

import os

from carwash.repositories.json_db import JsonDB
from carwash.repositories.user_repo import UserRepo
from carwash.repositories.vehicle_repo import VehicleRepo
from carwash.repositories.service_repo import ServiceRepo
from carwash.repositories.order_repo import OrderRepo
from carwash.repositories.account_repo import AccountRepo
from carwash.services.carwash_service import CarWashService
from carwash.services.auth_service import AuthService
from carwash.ui.menu import Menu


def main() -> None:
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "db.json")
    db = JsonDB(db_path)
    db.load()

    user_repo = UserRepo(db)
    vehicle_repo = VehicleRepo(db)
    service_repo = ServiceRepo(db)
    order_repo = OrderRepo(db)
    account_repo = AccountRepo(db)

    carwash_service = CarWashService(user_repo, vehicle_repo, service_repo, order_repo)
    auth_service = AuthService(account_repo)

    Menu(carwash_service, auth_service).run()


if __name__ == "__main__":
    main()
