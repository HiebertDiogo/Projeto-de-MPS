from typing import Dict, List, Optional
from entities import User, Vehicle


class UserDAO:
    def __init__(self) -> None:
        self._users_by_cpf: Dict[str, User] = {}

    def upsert_user_with_vehicle(self, user_data: dict, vehicle: Vehicle) -> User:
        cpf = user_data["cpf"]
        existing = self._users_by_cpf.get(cpf)

        if existing is None:
            user = User(
                name=user_data["name"],
                birth_date=user_data["birth_date"],
                email=user_data["email"],
                cpf=cpf,
                vehicles=[vehicle],
            )
            self._users_by_cpf[cpf] = user
            return user

        existing.vehicles.append(vehicle)
        return existing

    def list_users(self) -> List[User]:
        return list(self._users_by_cpf.values())

    def list_user_names(self) -> List[tuple]:
        return [(u.cpf, u.name) for u in self._users_by_cpf.values()]

    def get_by_cpf(self, cpf: str) -> Optional[User]:
        return self._users_by_cpf.get(cpf)