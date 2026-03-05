
from __future__ import annotations

from typing import List, Optional
from carwash.models.service_order import ServiceOrder
from carwash.repositories.json_db import JsonDB


class OrderRepo:
    def __init__(self, db: JsonDB):
        self.db = db

    def add(self, order: ServiceOrder) -> None:
        self.db.data["orders"].append(order.to_dict())
        self.db.save()

    def get_by_id(self, order_id: str) -> Optional[ServiceOrder]:
        for o in self.db.data["orders"]:
            if o["order_id"] == order_id:
                return ServiceOrder.from_dict(o)
        return None

    def list_all(self) -> List[ServiceOrder]:
        return [ServiceOrder.from_dict(o) for o in self.db.data["orders"]]
