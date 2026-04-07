from __future__ import annotations

from typing import List, Optional

from carwash.services.carwash_service import CarWashService
from carwash.services.auth_service import AuthService
from carwash.services.validators import validate_login, validate_password_iam_style

from carwash.strategy.discount_strategy import (
    NoDiscountStrategy,
    PercentDiscountStrategy,
    LoyaltyDiscountStrategy,
)


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
            print("9) Gerar relatório de estatísticas")
            print("10) Atualizar dados de usuário  [Memento]")
            print("11) Desfazer última atualização de usuário  [Memento]")
            print("12) Configurar desconto para ordens  [Strategy]")
            print("13) Resumo da sessão  [Observer]")
            print("14) Logout")
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
            elif op == "14":
                self.logout_flow()
            elif op == "9":
                self.generate_report_flow()
            elif op == "10":
                self.update_user_flow()
            elif op == "11":
                self.undo_user_update_flow()
            elif op == "12":
                self.configure_discount_flow()
            elif op == "13":
                self.session_summary_flow()
            elif op == "0":
                print("Saindo...")
                return
            else:
                print(" Opção inválida.")

    def create_account_flow(self) -> None:
        print("\n--- Criar conta ---")
        name  = self._input_non_empty("Nome: ")
        birth = self._input_non_empty("Data de nascimento (dd/mm/aaaa): ")
        email = self._input_non_empty("Email: ")
        cpf   = self._input_non_empty("CPF (somente números ou com máscara): ")

        ok, msg, user = self.carwash_service.register_user(name, birth, email, cpf)
        print((" " if ok else " ") + msg)
        if not ok or user is None:
            self._pause()
            return

        while True:
            login = input("Login (apenas letras, mínimo 3 caracteres): ").strip()
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
        login    = self._input_non_empty("Login: ")
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
        name  = self._input_non_empty("Nome: ")
        birth = self._input_non_empty("Data de nascimento (dd/mm/aaaa): ")
        email = self._input_non_empty("Email: ")
        cpf   = self._input_non_empty("CPF: ")

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
        users    = self.carwash_service.list_users()
        vehicles = self.carwash_service.list_vehicles()

        if not users:
            print("(vazio)")
            self._pause()
            return

        by_owner: dict = {}
        for v in vehicles:
            by_owner.setdefault(v.owner_user_id, []).append(v)

        for u in users:
            undo_flag = " [undo disponível]" if self.carwash_service.has_undo_snapshot(u.user_id) else ""
            print(f"\n- {u.name} | CPF: {u.cpf} | Email: {u.email} | Nasc: {u.birth_date}{undo_flag}")
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
            for idx, s in enumerate(services, start=1):
                print(f"{idx}) {s.name} | R$ {s.price_brl:.2f}")
        self._pause()

    def create_order_flow(self) -> None:
        if not self._require_login():
            return

        print("\n--- Criar atendimento (ordem de serviço) ---")
        print(f"  Desconto ativo: {self.carwash_service.get_discount_description()}")

        all_vehicles = self.carwash_service.list_vehicles()

        if not all_vehicles:
            print(" Não há veículos cadastrados no sistema.")
            self._pause()
            return

        print("Veículos disponíveis:")
        for idx, v in enumerate(all_vehicles, start=1):
            print(f"{idx}) {v.plate} - {v.model} (Dono ID: {v.owner_user_id})")

        while True:
            try:
                choice = int(self._input_non_empty("Escolha o veículo: "))
                if 1 <= choice <= len(all_vehicles):
                    vehicle        = all_vehicles[choice - 1]
                    target_user_id = vehicle.owner_user_id
                    break
            except ValueError:
                pass
            print(" Opção inválida.")

        services = self.carwash_service.list_services()
        if not services:
            print(" Não há serviços cadastrados. Cadastre primeiro (opção 4).")
            self._pause()
            return

        print("\nServiços disponíveis (separe números por vírgula):")
        for idx, s in enumerate(services, start=1):
            print(f"{idx}) {s.name} - R$ {s.price_brl:.2f}")

        raw   = self._input_non_empty("Serviços: ")
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

        ok, msg, order = self.carwash_service.create_order(target_user_id, vehicle.plate, picks)
        print(("" if ok else " ") + msg)
        if ok and order:
            print(f"Total: R$ {order.total_brl:.2f} | Data: {order.created_at}")
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

        timestamp   = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        filename    = f"relatorio_{timestamp}.{ext}"
        reports_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "reports")
        )
        output_path = os.path.join(reports_dir, filename)

        try:
            report       = self.carwash_service.build_report(fmt)
            written_path = report.generate(output_path)
            print(" Relatório gerado com sucesso!")
            print(f"  Arquivo: {written_path}")
        except Exception as exc:
            print(f" Erro ao gerar relatório: {exc}")

        self._pause()

    def list_orders_flow(self) -> None:
        print("\n--- Atendimentos (ordens de serviço) ---")
        orders       = self.carwash_service.list_orders()
        users        = {u.user_id: u for u in self.carwash_service.list_users()}
        services_map = {s.service_id: s for s in self.carwash_service.list_services()}
        if not orders:
            print("(vazio)")
            self._pause()
            return

        for idx, o in enumerate(orders, start=1):
            u     = users.get(o.user_id)
            uname = u.name if u else "Desconhecido"
            print(f"\n{idx}) Cliente: {uname} | Veículo: {o.vehicle_plate} | Total: R$ {o.total_brl:.2f} | {o.created_at}")
            print("  Serviços:")
            for sid in o.service_ids:
                s     = services_map.get(sid)
                sname = s.name if s else "(serviço removido)"
                price = f" - R$ {s.price_brl:.2f}" if s else ""
                print(f"    • {sname}{price}")

        self._pause()

    # ------------------------------------------------------------------ #
    #  MEMENTO – Atualizar / Desfazer usuário                             #
    # ------------------------------------------------------------------ #

    def update_user_flow(self) -> None:
        """
        [Memento] Permite editar nome, data de nascimento ou e-mail de um
        usuário. O estado anterior é salvo automaticamente como Memento.
        """
        if not self._require_login():
            return

        print("\n--- Atualizar dados de usuário  [Padrão: Memento] ---")
        users = self.carwash_service.list_users()
        if not users:
            print("Nenhum usuário cadastrado.")
            self._pause()
            return

        for idx, u in enumerate(users, start=1):
            print(f"{idx}) {u.name} | CPF: {u.cpf} | Email: {u.email} | Nasc: {u.birth_date}")

        while True:
            try:
                choice = int(self._input_non_empty("Escolha o usuário a atualizar: "))
                if 1 <= choice <= len(users):
                    target = users[choice - 1]
                    break
            except ValueError:
                pass
            print(" Opção inválida.")

        print(f"\nUsuário selecionado: {target.name}")
        print("Deixe em branco para manter o valor atual.")

        new_name  = input(f"Novo nome [{target.name}]: ").strip() or None
        new_birth = input(f"Nova data de nascimento [{target.birth_date}]: ").strip() or None
        new_email = input(f"Novo e-mail [{target.email}]: ").strip() or None

        ok, msg, updated = self.carwash_service.update_user(
            target.user_id, name=new_name, birth_date=new_birth, email=new_email
        )
        print((" " if ok else " ") + msg)
        if ok and updated:
            print(f"  Dados atuais: {updated.name} | {updated.birth_date} | {updated.email}")
            print("  (use a opção 'z' para desfazer esta alteração)")
        self._pause()

    def undo_user_update_flow(self) -> None:
        """
        [Memento] Desfaz a última atualização de um usuário,
        restaurando o snapshot guardado pelo Caretaker.
        """
        if not self._require_login():
            return

        print("\n--- Desfazer última atualização de usuário  [Padrão: Memento] ---")
        users = self.carwash_service.list_users()
        # Filtra apenas os que têm snapshot disponível
        with_snapshot = [u for u in users if self.carwash_service.has_undo_snapshot(u.user_id)]

        if not with_snapshot:
            print("Nenhum usuário com atualização pendente para desfazer.")
            self._pause()
            return

        for idx, u in enumerate(with_snapshot, start=1):
            print(f"{idx}) {u.name} | CPF: {u.cpf} | Email: {u.email}")

        while True:
            try:
                choice = int(self._input_non_empty("Escolha o usuário: "))
                if 1 <= choice <= len(with_snapshot):
                    target = with_snapshot[choice - 1]
                    break
            except ValueError:
                pass
            print(" Opção inválida.")

        ok, msg, restored = self.carwash_service.undo_last_user_update(target.user_id)
        print((" " if ok else " ") + msg)
        if ok and restored:
            print(f"  Dados restaurados: {restored.name} | {restored.birth_date} | {restored.email}")
        self._pause()

    # ------------------------------------------------------------------ #
    #  STRATEGY – Configurar desconto                                     #
    # ------------------------------------------------------------------ #

    def configure_discount_flow(self) -> None:
        """
        [Strategy] Permite escolher em runtime qual estratégia de desconto
        será aplicada ao criar novas ordens de serviço.
        """
        if not self._require_login():
            return

        print("\n--- Configurar desconto para ordens  [Padrão: Strategy] ---")
        print(f"  Estratégia atual: {self.carwash_service.get_discount_description()}")
        print()
        print("Estratégias disponíveis:")
        print("  1) Sem desconto")
        print("  2) Desconto fixo de 10%")
        print("  3) Desconto fixo de 20%")
        print("  4) Fidelidade: 15% a partir da 3ª ordem")

        choice = self._input_non_empty("Escolha: ").strip()

        if choice == "1":
            strategy = NoDiscountStrategy()
        elif choice == "2":
            strategy = PercentDiscountStrategy(10)
        elif choice == "3":
            strategy = PercentDiscountStrategy(20)
        elif choice == "4":
            strategy = LoyaltyDiscountStrategy()
        else:
            print(" Opção inválida.")
            self._pause()
            return

        self.carwash_service.set_discount_strategy(strategy)
        print(f" Estratégia definida: {strategy.description}")
        self._pause()

    # ------------------------------------------------------------------ #
    #  OBSERVER – Resumo da sessão                                        #
    # ------------------------------------------------------------------ #

    def session_summary_flow(self) -> None:
        """
        [Observer] Exibe o resumo acumulado pelo SummaryOrderObserver
        sobre as ordens criadas nesta sessão.
        """
        print("\n--- Resumo da sessão  [Padrão: Observer] ---")
        print(self.carwash_service.get_session_summary())
        self._pause()
