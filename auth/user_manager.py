from datetime import UTC, datetime

from auth.jwt_handler import create_token
from auth.password_hash import hash_password, verify_password
from database.models import DatabaseManager
from utils.validators import is_strong_password, is_valid_email


class UserManager:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def register(self, name: str, email: str, password: str) -> tuple[bool, str]:
        email = (email or "").strip().lower()
        if not name.strip():
            return False, "Name is required"
        if not is_valid_email(email):
            return False, "Invalid email format"
        if not is_strong_password(password):
            return False, "Password must be 8+ chars with upper, lower, and number"
        if self.db.users.find_one({"email": email}):
            return False, "Email already registered"

        user = {
            "name": name.strip(),
            "email": email,
            "password_hash": hash_password(password),
            "created_at": datetime.now(UTC),
            "last_login": None,
            "profile_picture": "",
            "phone": "",
            "is_verified": False,
        }
        self.db.users.insert_one(user)
        return True, "Registration successful"

    def login(self, email: str, password: str) -> tuple[bool, str, dict | None]:
        email = (email or "").strip().lower()
        user = self.db.users.find_one({"email": email})
        if not user or not verify_password(password, user.get("password_hash", "")):
            return False, "Invalid email or password", None

        self.db.users.update_one({"_id": user["_id"]}, {"$set": {"last_login": datetime.now(UTC)}})
        token = create_token(str(user["_id"]), user["email"])
        return True, token, {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}

    def update_profile(self, user_id: str, phone: str = "", profile_picture: str = "") -> tuple[bool, str]:
        from bson import ObjectId

        update = {"phone": (phone or "").strip(), "profile_picture": (profile_picture or "").strip()}
        result = self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update})
        if result.matched_count == 0:
            return False, "User not found"
        return True, "Profile updated"
