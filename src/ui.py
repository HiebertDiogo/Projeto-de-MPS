from user_manager import UserManager


class ClientManagerUI:
    def __init__(self, user_manager: UserManager, list_ui: "ClientListUI") -> None:
        self._user_manager = user_manager
        self._list_ui = list_ui

    def _prompt_non_empty(self, label: str) -> str:
        while True:
            value = input(label).strip()
            if value:
                return value
            print("Value cannot be empty.")

    def register_flow(self) -> None:
        print("\n=== USER / VEHICLE REGISTRATION ===")

        name = self._prompt_non_empty("Name: ")

        while True:
            birth_date = input("Birth date (dd/mm/yyyy): ").strip()
            if self._user_manager.validator.validate_date(birth_date):
                break
            print("Invalid date. Please use format dd/mm/yyyy.")

        while True:
            email = input("Email: ").strip()
            if self._user_manager.validator.validate_email(email):
                break
            print("Invalid email format.")

        while True:
            cpf = input("CPF: ").strip()
            if self._user_manager.validator.validate_cpf(cpf):
                break
            print("Invalid CPF. Please enter a valid 11-digit CPF.")

        while True:
            plate = input("Vehicle plate: ").strip()
            if self._user_manager.validator.validate_plate(plate):
                break
            print("Invalid plate format. Example: ABC1234 or ABC1D23")

        model = self._prompt_non_empty("Vehicle model: ")
        color = self._prompt_non_empty("Vehicle color: ")

        self._user_manager.register_user_vehicle(
            name=name,
            birth_date=birth_date,
            email=email,
            cpf=cpf,
            plate=plate,
            model=model,
            color=color,
        )

        print("\nUser/vehicle successfully registered!\n")

    def menu(self) -> None:
        while True:
            print("=== CAR WASH SYSTEM - USER MANAGEMENT ===")
            print("1 - Register user/vehicle")
            print("2 - List users (detailed)")
            print("3 - List user names only")
            print("4 - Exit")
            option = input("Choose an option: ").strip()

            if option == "1":
                self.register_flow()
            elif option == "2":
                self._list_ui.show_users_detailed()
            elif option == "3":
                self._list_ui.show_user_names()
            elif option == "4":
                print("\nClosing the system... Goodbye!\n")
                break
            else:
                print("\nInvalid option. Please try again.\n")


class ClientListUI:
    def __init__(self, user_manager: UserManager) -> None:
        self._user_manager = user_manager

    def show_users_detailed(self) -> None:
        print("\n=== USERS LIST ===")

        users = self._user_manager.list_users_detailed()
        if not users:
            print("No users registered.\n")
            return

        counter = 1
        for user in users:
            print(f"\nUser {counter}:")
            print(f"  Name: {user.name}")
            print(f"  CPF: {user.cpf}")
            print(f"  Birth date: {user.birth_date}")
            print(f"  Email: {user.email}")
            print("  Vehicles:")

            for v in user.vehicles:
                print(f"    - Plate: {v.plate} | Model: {v.model} | Color: {v.color}")

            counter += 1

        print()

    def show_user_names(self) -> None:
        print("\n=== REGISTERED USER NAMES ===")

        items = self._user_manager.list_user_names()
        if not items:
            print("No users registered.\n")
            return

        counter = 1
        for cpf, name in items:
            print(f"{counter}. {name} (CPF: {cpf})")
            counter += 1

        print()