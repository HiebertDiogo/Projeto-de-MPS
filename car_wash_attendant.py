class CarWashAttendant:
    def __init__(self):
        self.records = []

    def register_user(self):
        print("\n=== USER / VEHICLE REGISTRATION ===")
        name = input("Name: ").strip()
        birth_date = input("Birth date (dd/mm/yyyy): ").strip()
        email = input("Email: ").strip()
        cpf = input("CPF: ").strip()
        plate = input("Vehicle plate: ").strip()
        model = input("Vehicle model: ").strip()
        color = input("Vehicle color: ").strip()

        record = {
            "name": name,
            "birth_date": birth_date,
            "email": email,
            "cpf": cpf,
            "plate": plate,
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
