import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from utils.logger import get_logger

logger = get_logger(__name__)
MONGO_SERVER_API_VERSION = "1"


class MongoConnection:
    _client = None

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            cls._client = MongoClient(uri, server_api=ServerApi(MONGO_SERVER_API_VERSION), connect=False)
        return cls._client

    @classmethod
    def get_database(cls):
        db_name = os.getenv("MONGODB_DB_NAME", "ai_career_intel")
        return cls.get_client()[db_name]
