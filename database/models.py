from datetime import UTC, datetime
from typing import Any

from pymongo import ASCENDING
from pymongo.errors import OperationFailure

from database.connection import MongoConnection
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    def __init__(self) -> None:
        self.db = MongoConnection.get_database()
        self.users = self.db["users"]
        self.resumes = self.db["resumes"]
        self.interview_sessions = self.db["interview_sessions"]
        self.job_descriptions = self.db["job_descriptions"]
        self.analytics = self.db["analytics"]
        self.ensure_collections()

    def ensure_collections(self) -> None:
        for action in [
            lambda: self.users.create_index([("email", ASCENDING)], unique=True),
            lambda: self.resumes.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)]),
            lambda: self.interview_sessions.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)]),
            lambda: self.job_descriptions.create_index([("user_id", ASCENDING), ("created_at", ASCENDING)]),
            lambda: self.analytics.create_index([("user_id", ASCENDING)], unique=True),
        ]:
            try:
                action()
            except OperationFailure as exc:
                logger.warning("Index creation skipped: %s", exc)

        validators = {
            "users": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["name", "email", "password_hash", "created_at"],
                    "properties": {
                        "email": {"bsonType": "string"},
                        "password_hash": {"bsonType": "string"},
                    },
                }
            },
            "resumes": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["user_id", "file_name", "skills", "created_at"],
                }
            },
            "interview_sessions": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["user_id", "role", "questions", "answers", "created_at"],
                }
            },
        }

        for collection, validator in validators.items():
            try:
                # Use moderate validation so legacy documents remain readable while
                # all new inserts/updates are validated against the schema.
                self.db.command({"collMod": collection, "validator": validator, "validationLevel": "moderate"})
            except OperationFailure:
                logger.info("Validator update skipped for %s", collection)

    def upsert_analytics(self, user_id: Any, ats: float | None = None, interview: float | None = None, skills: list[str] | None = None) -> None:
        update: dict[str, Any] = {"$setOnInsert": {"created_at": datetime.now(UTC), "user_id": user_id}}
        if ats is not None:
            update.setdefault("$push", {})["ats_scores"] = ats
        if interview is not None:
            update.setdefault("$push", {})["interview_scores"] = interview
        if skills is not None:
            update.setdefault("$set", {})["skill_improvements"] = skills
        self.analytics.update_one({"user_id": user_id}, update, upsert=True)
