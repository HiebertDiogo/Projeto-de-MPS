import re
from datetime import datetime


class ValidationManager:
    def validate_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r"\D", "", cpf)
        return len(cpf) == 11

    def validate_email(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def validate_date(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validate_plate(self, plate: str) -> bool:
        clean_plate = plate.replace("-", "").upper()
        pattern = r"^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$"
        return re.match(pattern, clean_plate) is not None