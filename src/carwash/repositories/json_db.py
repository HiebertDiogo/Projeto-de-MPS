
"""
Very small JSON "database".

Schema (db.json):
{
  "users": [],
  "vehicles": [],
  "services": [],
  "orders": [],
  "accounts": []
}
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict


DEFAULT_DB: Dict[str, Any] = {
    "users": [],
    "vehicles": [],
    "services": [],
    "orders": [],
    "accounts": [],
}


class JsonDB:
    def __init__(self, path: str):
        self.path = path
        self._data: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._data = dict(DEFAULT_DB)
            self.save()
            return self._data

        with open(self.path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

        # ensure keys exist
        for k, v in DEFAULT_DB.items():
            self._data.setdefault(k, v if not isinstance(v, list) else [])
        return self._data

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    @property
    def data(self) -> Dict[str, Any]:
        return self._data
