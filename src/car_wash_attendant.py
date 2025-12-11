import re
from datetime import datetime

class CarWashAttendant:
    def __init__(self):
        self.records = []

    def _validate_cpf(self, cpf):

        cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11:
            return False
            
        return True

    def _validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def _validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def _validate_plate(self, plate):
        # format (ABC-1234) and Mercosul (ABC1D23)
        # Removing hyphens for validation
        clean_plate = plate.replace("-", "").upper()
        # Basic regex for Brazil plates
        pattern = r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$'
        return re.match(pattern, clean_plate) is not None

    def register_user(self):
        print("\n=== USER / VEHICLE REGISTRATION ===")
        
        while True:
            name = input("Name: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        while True:
            birth_date = input("Birth date (dd/mm/yyyy): ").strip()
            if self._validate_date(birth_date):
                break
            print("Invalid date. Please use format dd/mm/yyyy.")

        while True:
            email = input("Email: ").strip()
            if self._validate_email(email):
                break
            print("Invalid email format.")

        while True:
            cpf = input("CPF: ").strip()
            if self._validate_cpf(cpf):
                break
            print("Invalid CPF. Please enter a valid 11-digit CPF.")

        while True:
            plate = input("Vehicle plate: ").strip()
            if self._validate_plate(plate):
                break
            print("Invalid plate format. Example: ABC1234 or ABC1D23")

        while True:
            model = input("Vehicle model: ").strip()
            if model:
                break
            print("Model cannot be empty.")

        while True:
            color = input("Vehicle color: ").strip()
            if color:
                break
            print("Color cannot be empty.")

        record = {
            "name": name,
            "birth_date": birth_date,
            "email": email,
            "cpf": re.sub(r'\D', '', cpf), # Store only numbers
            "plate": plate.upper(),
            "model": model,
            "color": color,
        }

        self.records.append(record)
        print("\nUser/vehicle successfully registered!\n")

    def list_users(self):
        print("\n=== USERS LIST ===")

        if not self.records:
            print("No users registered.\n")
            return

        users_by_cpf = {}

        for r in self.records:
            cpf = r["cpf"]
            if cpf not in users_by_cpf:
                users_by_cpf[cpf] = {
                    "name": r["name"],
                    "birth_date": r["birth_date"],
                    "email": r["email"],
                    "cpf": r["cpf"],
                    "vehicles": []
                }

            vehicle = {
                "plate": r["plate"],
                "model": r["model"],
                "color": r["color"]
            }
            users_by_cpf[cpf]["vehicles"].append(vehicle)

        counter = 1
        for cpf, data in users_by_cpf.items():
            print(f"\nUser {counter}:")
            print(f"  Name: {data['name']}")
            print(f"  CPF: {data['cpf']}")
            print(f"  Birth date: {data['birth_date']}")
            print(f"  Email: {data['email']}")
            print("  Vehicles:")

            for v in data["vehicles"]:
                print(f"    - Plate: {v['plate']} | Model: {v['model']} | Color: {v['color']}")

            counter += 1

        print() 

    def list_user_names(self):
        print("\n=== REGISTERED USER NAMES ===")

        if not self.records:
            print("No users registered.\n")
            return

        names_by_cpf = {}

        for r in self.records:
            cpf = r["cpf"]
            if cpf not in names_by_cpf:
                names_by_cpf[cpf] = r["name"]

        counter = 1
        for cpf, name in names_by_cpf.items():
            print(f"{counter}. {name} (CPF: {cpf})")
            counter += 1

        print()

    def menu(self):
        while True:
            print("=== CAR WASH SYSTEM - USER MANAGEMENT ===")
            print("1 - Register user/vehicle")
            print("2 - List users (detailed)")
            print("3 - List user names only")
            print("4 - Exit")
            option = input("Choose an option: ").strip()

            if option == "1":
                self.register_user()
            elif option == "2":
                self.list_users()
            elif option == "3":
                self.list_user_names()
            elif option == "4":
                print("\nClosing the system... Goodbye!\n")
                break
            else:
                print("\nInvalid option. Please try again.\n")
