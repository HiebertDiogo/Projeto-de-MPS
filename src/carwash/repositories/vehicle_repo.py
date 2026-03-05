
from __future__ import annotations

from typing import List, Optional
from carwash.models.vehicle import Vehicle
from carwash.repositories.json_db import JsonDB


class VehicleRepo:
    def __init__(self, db: JsonDB):
        self.db = db

    def add(self, vehicle: Vehicle) -> None:
        self.db.data["vehicles"].append(vehicle.to_dict())
        self.db.save()

    def list_by_user(self, user_id: str) -> List[Vehicle]:
        return [Vehicle.from_dict(v) for v in self.db.data["vehicles"] if v["owner_user_id"] == user_id]

    def get_by_plate(self, plate: str) -> Optional[Vehicle]:
        plate_u = (plate or "").upper()
        for v in self.db.data["vehicles"]:
            if v["plate"].upper() == plate_u:
                return Vehicle.from_dict(v)
        return None

    def list_all(self) -> List[Vehicle]:
        return [Vehicle.from_dict(v) for v in self.db.data["vehicles"]]
