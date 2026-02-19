import re
from entities import Vehicle
from user_dao import UserDAO
from validation_manager import ValidationManager


class UserManager:
    def __init__(self, dao: UserDAO, validator: ValidationManager) -> None:
        self._dao = dao
        self._validator = validator

    def register_user_vehicle(
        self,
        *,
        name: str,
        birth_date: str,
        email: str,
        cpf: str,
        plate: str,
        model: str,
        color: str,
    ) -> None:

        cpf_digits = re.sub(r"\D", "", cpf)
        plate_up = plate.upper()

        user_data = {
            "name": name,
            "birth_date": birth_date,
            "email": email,
            "cpf": cpf_digits,
        }

        vehicle = Vehicle(plate=plate_up, model=model, color=color)
        self._dao.upsert_user_with_vehicle(user_data, vehicle)

    def list_users_detailed(self):
        return self._dao.list_users()

    def list_user_names(self):
        return self._dao.list_user_names()

    @property
    def validator(self) -> ValidationManager:
        return self._validator