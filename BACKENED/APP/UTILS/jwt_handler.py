from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

from app.config import settings


# ==========================================
# 🔐 CONFIGURATION
# ==========================================

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ==========================================
# 🪪 CREATE ACCESS TOKEN
# ==========================================
def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================
# 🔄 CREATE REFRESH TOKEN
# ==========================================
def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================
# ✅ VERIFY TOKEN
# ==========================================
def verify_token(token: str, token_type: Optional[str] = None) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if token_type and payload.get("type") != token_type:
            raise JWTError("Invalid token type")

        return payload

    except JWTError:
        return None


# ==========================================
# 🔁 REFRESH ACCESS TOKEN
# ==========================================
def refresh_access_token(refresh_token: str) -> Optional[str]:
    payload = verify_token(refresh_token, token_type="refresh")

    if not payload:
        return None

    new_access_token = create_access_token({
        "user_id": payload["user_id"],
        "email": payload["email"],
        "role": payload["role"]
    })

    return new_access_token