
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Service:
    service_id: str
    name: str
    price_brl: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "price_brl": self.price_brl,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Service":
        return Service(
            service_id=d["service_id"],
            name=d["name"],
            price_brl=float(d["price_brl"]),
        )
