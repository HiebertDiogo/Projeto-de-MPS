from carwash.commands.base_command import Command
from carwash.models.user import User
from uuid import uuid4

class RegisterUserCommand(Command):
    def __init__(self, user_repo, logger, name, birth_date, email, cpf_clean):
        self.user_repo = user_repo
        self.logger = logger
        self.name = name
        self.birth_date = birth_date
        self.email = email
        self.cpf_clean = cpf_clean
        self.result = None 

    def execute(self):
        user = User(
            user_id=str(uuid4()),
            name=self.name,
            birth_date=self.birth_date,
            email=self.email,
            cpf=self.cpf_clean,
        )
        self.user_repo.add(user)
        self.logger.log_info("Command: User registered", {"user_id": user.user_id, "cpf": user.cpf})
        self.result = user
        return user
    