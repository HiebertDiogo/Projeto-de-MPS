
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Vehicle:
    plate: str
    model: str
    color: str
    owner_user_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plate": self.plate,
            "model": self.model,
            "color": self.color,
            "owner_user_id": self.owner_user_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Vehicle":
        return Vehicle(
            plate=d["plate"],
            model=d["model"],
            color=d["color"],
            owner_user_id=d["owner_user_id"],
        )
