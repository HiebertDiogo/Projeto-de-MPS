from carwash.commands.base_command import Command
from carwash.models.service import Service
from uuid import uuid4

class CreateServiceCommand(Command):
    def __init__(self, service_repo, logger, name, price_brl):
        self.service_repo = service_repo
        self.logger = logger
        self.name = name
        self.price_brl = price_brl

    def execute(self) -> Service:
        s = Service(
            service_id=str(uuid4()),
            name=self.name,
            price_brl=float(self.price_brl),
        )
        
        self.service_repo.add(s)
        
        self.logger.log_info("Command: Service created", {
            "service_id": s.service_id, 
            "name": s.name, 
            "price": s.price_brl
        })
        
        return s