from carwash.commands.base_command import Command
from carwash.models.service_order import ServiceOrder
from datetime import datetime
from uuid import uuid4

class CreateOrderCommand(Command):
    def __init__(self, order_repo, logger, user_id, vehicle_plate, service_ids, total_brl):
        self.order_repo = order_repo
        self.logger = logger
        self.user_id = user_id
        self.vehicle_plate = vehicle_plate
        self.service_ids = service_ids
        self.total_brl = total_brl

    def execute(self) -> ServiceOrder:
        order = ServiceOrder(
            order_id=str(uuid4()),
            user_id=self.user_id,
            vehicle_plate=self.vehicle_plate,
            service_ids=list(self.service_ids),
            created_at=datetime.now().isoformat(timespec="seconds"),
            total_brl=round(float(self.total_brl), 2),
        )
        
        self.order_repo.add(order)
        
        self.logger.log_info("Command: Service order created", {
            "order_id": order.order_id, 
            "total": order.total_brl,
            "services_count": len(order.service_ids)
        })
        
        return order