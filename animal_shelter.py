"""animal_shelter.py"""
"""Reusable create-and-read wrapper for AAC.animals"""
"""Author: Chris Davidson"""
"""Course : CS-340"""

import os
from typing import Any, Dict, List, Optional

import certifi
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class AnimalShelter:
    """Create-and-read wrapper for AAC.animals."""

    def __init__(
        self,
        user: str = os.getenv("MONGO_USER", "aacuser"),
        password: str = os.getenv("MONGO_PASS", "StrongPassword42!"),
        host: str = os.getenv("MONGO_HOST", "nv-desktop-services.apporto.com"),
        port: int = int(os.getenv("MONGO_PORT", 31373)),
        db_name: str = "AAC",
        col_name: str = "animals",
        auth_source: str = "admin",
    ) -> None:
        uri = (
            f"mongodb://{user}:{password}@{host}:{port}"
            f"/?authSource={auth_source}"
        )
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)

        self.database = self.client[db_name]
        self.collection: Collection = self.database[col_name]
        # Verify credentials immediately
        self.client.admin.command("ping")

    # ------------------------ Create ------------------------
    def create(self, data: Dict[str, Any]) -> bool:
        """Insert *data* into the collection; return True on success."""
        if not isinstance(data, dict) or not data:
            raise ValueError("`data` must be a non-empty dict")
        try:
            return bool(self.collection.insert_one(data).inserted_id)
        except PyMongoError as err:
            print(f"[ERROR] create(): {err}")
            return False

    # ------------------------ Read ------------------------
    def read(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict[str, int]] = None,
    ) -> List[Dict[str, Any]]:
        """Return a list of documents matching *query* (may be empty)."""
        if not isinstance(query, dict):
            raise ValueError("`query` must be a dict")
        try:
            return list(self.collection.find(query, projection))
        except PyMongoError as err:
            print(f"[ERROR] read(): {err}")
            return []

    # ----------------------- Update -----------------------
    def update(self, query: dict, new_values: dict) -> int:
        """Update all documents matching *query* with *new_values*."""
        """Returns the number of modified documents."""
        if not query or not new_values:
            raise ValueError("query and new_values must be non-empty dicts")
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as err:
            print(f"[ERROR] update(): {err}")
            return 0

    # ------------------------ Delete ------------------------
    def delete(self, query: dict) -> int:
        """Delete all documents matching *query*."""
        """Returns the number of removed documents."""
        if not query:
            raise ValueError("query must be a non-empty dict")
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as err:
            print(f"[ERROR] delete(): {err}")
            return 0
