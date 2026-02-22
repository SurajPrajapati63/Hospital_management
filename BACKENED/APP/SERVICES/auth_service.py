from datetime import datetime
from typing import Optional
from bson import ObjectId

from app.database import db
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
)
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


# ==========================================
# 👤 REGISTER USER
# ==========================================
async def register_user(payload: UserRegister):

    existing_user = db.users.find_one({"email": payload.email})
    if existing_user:
        raise Exception("User already exists")

    hashed_pw = hash_password(payload.password)

    user_data = {
        "email": payload.email,
        "full_name": payload.full_name,
        "role": payload.role,
        "password": hashed_pw,
        "created_at": datetime.utcnow(),
    }

    result = db.users.insert_one(user_data)
    user_id = str(result.inserted_id)

    access_token = create_access_token({
        "user_id": user_id,
        "email": payload.email,
        "role": payload.role,
    })

    refresh_token = create_refresh_token({
        "user_id": user_id,
        "email": payload.email,
        "role": payload.role,
    })

    logger.info(f"User registered: {payload.email}")

    return {
        "user_id": user_id,
        "email": payload.email,
        "full_name": payload.full_name,
        "role": payload.role,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# ==========================================
# 🔐 LOGIN USER
# ==========================================
async def login_user(payload: UserLogin):

    user = db.users.find_one({"email": payload.email})
    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(payload.password, user["password"]):
        raise Exception("Invalid credentials")

    user_id = str(user["_id"])

    access_token = create_access_token({
        "user_id": user_id,
        "email": user["email"],
        "role": user["role"],
    })

    refresh_token = create_refresh_token({
        "user_id": user_id,
        "email": user["email"],
        "role": user["role"],
    })

    logger.info(f"User logged in: {payload.email}")

    return {
        "user_id": user_id,
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# ==========================================
# 🔁 REFRESH ACCESS TOKEN
# ==========================================
async def refresh_access(refresh_token: str):

    payload = verify_token(refresh_token, token_type="refresh")

    if not payload:
        raise Exception("Invalid refresh token")

    new_access_token = create_access_token({
        "user_id": payload["user_id"],
        "email": payload["email"],
        "role": payload["role"],
    })

    return {"access_token": new_access_token}


# ==========================================
# 🧑 GET CURRENT USER
# ==========================================
async def get_user_by_id(user_id: str):

    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    return {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
    }