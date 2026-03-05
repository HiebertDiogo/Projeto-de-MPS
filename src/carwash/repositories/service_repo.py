
from __future__ import annotations

from typing import List, Optional
from carwash.models.service import Service
from carwash.repositories.json_db import JsonDB


class ServiceRepo:
    def __init__(self, db: JsonDB):
        self.db = db

    def add(self, service: Service) -> None:
        self.db.data["services"].append(service.to_dict())
        self.db.save()

    def get_by_id(self, service_id: str) -> Optional[Service]:
        for s in self.db.data["services"]:
            if s["service_id"] == service_id:
                return Service.from_dict(s)
        return None

    def list_all(self) -> List[Service]:
        return [Service.from_dict(s) for s in self.db.data["services"]]
