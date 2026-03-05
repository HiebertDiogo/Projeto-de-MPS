
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass(frozen=True)
class ServiceOrder:
    order_id: str
    user_id: str
    vehicle_plate: str
    service_ids: List[str]
    created_at: str  # ISO string
    total_brl: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "vehicle_plate": self.vehicle_plate,
            "service_ids": list(self.service_ids),
            "created_at": self.created_at,
            "total_brl": self.total_brl,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ServiceOrder":
        return ServiceOrder(
            order_id=d["order_id"],
            user_id=d["user_id"],
            vehicle_plate=d["vehicle_plate"],
            service_ids=list(d["service_ids"]),
            created_at=d["created_at"],
            total_brl=float(d["total_brl"]),
        )
