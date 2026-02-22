from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    AuthResponse,
    Token,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest,
    UserResponse,
)

from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access,
    get_user_by_id,
)

from app.utils.jwt_handler import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==================================
# 📝 REGISTER
# ==================================
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    try:
        return register_user(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 🔐 LOGIN
# ==================================
@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin):
    try:
        user = login_user(payload)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


# ==================================
# 🔁 REFRESH TOKEN
# ==================================
@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshTokenRequest):
    try:
        return refresh_access(payload.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ==================================
# 👤 GET CURRENT USER
# ==================================
@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user