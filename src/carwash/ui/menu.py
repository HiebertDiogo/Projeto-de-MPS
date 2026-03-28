

from __future__ import annotations

from typing import List, Optional

from carwash.services.carwash_service import CarWashService
from carwash.services.auth_service import AuthService
from carwash.services.validators import validate_login, validate_password_iam_style


class Menu:
    def __init__(self, carwash_service: CarWashService, auth_service: AuthService):
        self.carwash_service = carwash_service
        self.auth_service = auth_service
        self.logged_user_id: Optional[str] = None

    # -------- helpers --------
    @staticmethod
    def _input_non_empty(prompt: str) -> str:
        while True:
            v = input(prompt).strip()
            if v:
                return v
            print(" Campo não pode ser vazio.")

    @staticmethod
    def _pause() -> None:
        input("\nEnter para continuar...")

    # -------- flows --------
    def run(self) -> None:
        while True:
            print("\n=== Lava Jato (OOP + JSON) ===")
            print("1) Criar conta")
            print("2) Login")
            print("3) Cadastrar usuário + veículo (precisa estar logado)")
            print("4) Cadastrar serviço (precisa estar logado)")
            print("5) Listar usuários")
            print("6) Listar serviços")
            print("7) Criar atendimento (ordem de serviço) (precisa estar logado)")
            print("8) Listar atendimentos")
            print("9) Logout")
            print("r) Gerar relatório de estatísticas")
            print("0) Sair")

            op = input("Escolha: ").strip()
            if op == "1":
                self.create_account_flow()
            elif op == "2":
                self.login_flow()
            elif op == "3":
                self.register_user_and_vehicle_flow()
            elif op == "4":
                self.create_service_flow()
            elif op == "5":
                self.list_users_flow()
            elif op == "6":
                self.list_services_flow()
            elif op == "7":
                self.create_order_flow()
            elif op == "8":
                self.list_orders_flow()
            elif op == "9":
                self.logout_flow()
            elif op == "r":
                self.generate_report_flow()
            elif op == "0":
                print("Saindo...")
                return
            else:
                print(" Opção inválida.")

    def create_account_flow(self) -> None:
        print("\n--- Criar conta ---")
        # Para associar conta ao usuário, primeiro cadastramos usuário (mínimo) ou reutilizamos por CPF.
        name = self._input_non_empty("Nome: ")
        birth = self._input_non_empty("Data de nascimento (dd/mm/aaaa): ")
        email = self._input_non_empty("Email: ")
        cpf = self._input_non_empty("CPF (somente números ou com máscara): ")

        ok, msg, user = self.carwash_service.register_user(name, birth, email, cpf)
        print((" " if ok else " ") + msg)
        if not ok or user is None:
            self._pause()
            return

        while True:
            login = input("Login (12 letras, sem números): ").strip()
            ok_login, msg_login = validate_login(login)
            if ok_login:
                break
            print("", msg_login)

        while True:
            password = input("Senha (IAM): ").strip()
            ok_pwd, msg_pwd = validate_password_iam_style(password, login)
            if ok_pwd:
                break
            print("", msg_pwd)

        ok, msg = self.auth_service.create_account(user.user_id, login, password)
        print((" " if ok else " ") + msg)
        self._pause()

    def login_flow(self) -> None:
        print("\n--- Login ---")
        login = self._input_non_empty("Login: ")
        password = self._input_non_empty("Senha: ")
        ok, msg, user_id = self.auth_service.authenticate(login, password)
        print((" " if ok else " ") + msg)
        if ok:
            self.logged_user_id = user_id
        self._pause()

    def logout_flow(self) -> None:
        self.logged_user_id = None
        print(" Logout efetuado.")
        self._pause()

    def _require_login(self) -> bool:
        if not self.logged_user_id:
            print("Você precisa estar logado para isso.")
            self._pause()
            return False
        return True

    def register_user_and_vehicle_flow(self) -> None:
        if not self._require_login():
            return

        print("\n--- Cadastrar usuário + veículo ---")
        # Permite cadastrar outro usuário (ex.: gerente cadastrando clientes),
        # mas exige estar logado (requisito do professor: validações de login).
        name = self._input_non_empty("Nome: ")
        birth = self._input_non_empty("Data de nascimento (dd/mm/aaaa): ")
        email = self._input_non_empty("Email: ")
        cpf = self._input_non_empty("CPF: ")

        ok, msg, user = self.carwash_service.register_user(name, birth, email, cpf)
        print((" " if ok else " ") + msg)
        if not ok or user is None:
            self._pause()
            return

        plate = self._input_non_empty("Placa: ")
        model = self._input_non_empty("Modelo: ")
        color = self._input_non_empty("Cor: ")
        ok, msg = self.carwash_service.add_vehicle(user.user_id, plate, model, color)
        print((" " if ok else " ") + msg)
        self._pause()

    def create_service_flow(self) -> None:
        if not self._require_login():
            return
        print("\n--- Cadastrar serviço ---")
        name = self._input_non_empty("Nome do serviço: ")
        while True:
            try:
                price = float(self._input_non_empty("Preço (R$): ").replace(",", "."))
                break
            except ValueError:
                print("Preço inválido.")
        ok, msg, _ = self.carwash_service.create_service(name, price)
        print((" " if ok else " ") + msg)
        self._pause()

    def list_users_flow(self) -> None:
        print("\n--- Usuários ---")
        users = self.carwash_service.list_users()
        vehicles = self.carwash_service.list_vehicles()

        if not users:
            print("(vazio)")
            self._pause()
            return

        # group vehicles by owner
        by_owner = {}
        for v in vehicles:
            by_owner.setdefault(v.owner_user_id, []).append(v)

        for u in users:
            print(f"\n- {u.name} | CPF: {u.cpf} | Email: {u.email} | Nasc: {u.birth_date}")
            vs = by_owner.get(u.user_id, [])
            if not vs:
                print("  Veículos: (nenhum)")
            else:
                print("  Veículos:")
                for v in vs:
                    print(f"    • {v.plate} - {v.model} ({v.color})")

        self._pause()

    def list_services_flow(self) -> None:
        print("\n--- Serviços ---")
        services = self.carwash_service.list_services()
        if not services:
            print("(vazio)")
        else:
            for s in services:
                print(f"- {s.service_id} | {s.name} | R$ {s.price_brl:.2f}")
        self._pause()

    def create_order_flow(self) -> None:
        if not self._require_login():
            return

        print("\n--- Criar atendimento (ordem de serviço) ---")
        # choose a vehicle for logged user (to keep simple and consistent)
        my_vehicles = self.carwash_service.list_vehicles_by_user(self.logged_user_id)
        if not my_vehicles:
            print(" Você não tem veículos cadastrados. Cadastre primeiro (opção 3).")
            self._pause()
            return

        print("Seus veículos:")
        for idx, v in enumerate(my_vehicles, start=1):
            print(f"{idx}) {v.plate} - {v.model} ({v.color})")

        while True:
            try:
                choice = int(self._input_non_empty("Escolha o veículo: "))
                if 1 <= choice <= len(my_vehicles):
                    vehicle = my_vehicles[choice - 1]
                    break
            except ValueError:
                pass
            print(" Opção inválida.")

        services = self.carwash_service.list_services()
        if not services:
            print(" Não há serviços cadastrados. Cadastre primeiro (opção 4).")
            self._pause()
            return

        print("\nServiços disponíveis (digite os números separados por vírgula):")
        for idx, s in enumerate(services, start=1):
            print(f"{idx}) {s.name} - R$ {s.price_brl:.2f}")

        raw = self._input_non_empty("Serviços: ")
        picks = []
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                i = int(part)
                if 1 <= i <= len(services):
                    picks.append(services[i - 1].service_id)
            except ValueError:
                continue

        ok, msg, order = self.carwash_service.create_order(self.logged_user_id, vehicle.plate, picks)
        print(("" if ok else " ") + msg)
        if ok and order:
            print(f"Ordem: {order.order_id} | Total: R$ {order.total_brl:.2f} | Data: {order.created_at}")
        self._pause()

    def generate_report_flow(self) -> None:
        import os
        from datetime import datetime

        print("\n--- Gerar relatório de estatísticas ---")
        print("Formatos disponíveis:")
        print("  1) HTML")
        print("  2) TXT")

        fmt_choice = self._input_non_empty("Escolha o formato (1 ou 2): ")
        if fmt_choice == "1":
            fmt, ext = "html", "html"
        elif fmt_choice == "2":
            fmt, ext = "txt", "txt"
        else:
            print(" Formato inválido. Escolha 1 (HTML) ou 2 (TXT).")
            self._pause()
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{timestamp}.{ext}"
        reports_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "reports")
        )
        output_path = os.path.join(reports_dir, filename)

        try:
            report = self.carwash_service.build_report(fmt)
            written_path = report.generate(output_path)
            print(" Relatório gerado com sucesso!")
            print(f"  Arquivo: {written_path}")
        except Exception as exc:
            print(f" Erro ao gerar relatório: {exc}")

        self._pause()

    def list_orders_flow(self) -> None:
        print("\n--- Atendimentos (ordens de serviço) ---")
        orders = self.carwash_service.list_orders()
        users = {u.user_id: u for u in self.carwash_service.list_users()}
        if not orders:
            print("(vazio)")
            self._pause()
            return

        for o in orders:
            u = users.get(o.user_id)
            uname = u.name if u else "Desconhecido"
            print(f"\n- {o.order_id} | Cliente: {uname} | Veículo: {o.vehicle_plate} | Total: R$ {o.total_brl:.2f} | {o.created_at}")
            print("  Serviços:")
            for sid in o.service_ids:
                print(f"    • {sid}")

        self._pause()
