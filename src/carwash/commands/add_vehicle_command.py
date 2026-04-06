from carwash.commands.base_command import Command
from carwash.models.vehicle import Vehicle

class AddVehicleCommand(Command):
    def __init__(self, vehicle_repo, logger, plate, model, color, owner_user_id):
        self.vehicle_repo = vehicle_repo
        self.logger = logger
        self.plate = plate
        self.model = model
        self.color = color
        self.owner_user_id = owner_user_id

    def execute(self):
        # Criando a Dataclass Vehicle exatamente com os campos que você postou
        v = Vehicle(
            plate=self.plate,
            model=self.model,
            color=self.color,
            owner_user_id=self.owner_user_id,
        )
        
        self.vehicle_repo.add(v)
        
        self.logger.log_info("Command: Vehicle registered", {
            "plate": v.plate, 
            "owner": v.owner_user_id
        })
        return v