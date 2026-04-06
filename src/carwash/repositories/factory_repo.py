import os
from .json_db import JsonDB
from .user_repo import UserRepo
from .vehicle_repo import VehicleRepo
from .service_repo import ServiceRepo
from .order_repo import OrderRepo
from .account_repo import AccountRepo

class FactoryRepo:
    _db = None

    @classmethod
    def _get_db(cls):
        if cls._db is None:
            db_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "db.json")
            cls._db = JsonDB(db_path)
            cls._db.load()
        return cls._db

    @classmethod
    def get_repository(cls, repo_type: str):
        db = cls._get_db()
        
        repos = {
            "user": UserRepo,
            "vehicle": VehicleRepo,
            "service": ServiceRepo,
            "order": OrderRepo,
            "account": AccountRepo
        }
        
        repo_class = repos.get(repo_type.lower())
        if repo_class:
            return repo_class(db)
        raise ValueError(f"O repositório '{repo_type}' não foi encontrado na Factory.")