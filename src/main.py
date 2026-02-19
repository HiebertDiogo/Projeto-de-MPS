from user_dao import UserDAO
from user_manager import UserManager
from ui import ClientListUI, ClientManagerUI
from validation_manager import ValidationManager


def main():
    dao = UserDAO()
    validator = ValidationManager()
    manager = UserManager(dao=dao, validator=validator)

    list_ui = ClientListUI(user_manager=manager)
    ui = ClientManagerUI(user_manager=manager, list_ui=list_ui)

    ui.menu()


if __name__ == "__main__":
    main()