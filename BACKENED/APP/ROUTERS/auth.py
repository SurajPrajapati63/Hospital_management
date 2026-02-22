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

# from services.auth_services import (
#     register_user,
#     authenticate_user,
#     refresh_access_token,
#     get_current_user_service,
#     request_password_reset,
#     confirm_password_reset,
#     change_user_password,
# )

from app.utils.jwt_handler import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==================================
# 📝 REGISTER
# ==================================
@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    try:
        return await register_user(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 🔐 LOGIN
# ==================================
@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin):
    user = await authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return user


# ==================================
# 🔁 REFRESH TOKEN
# ==================================
@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshTokenRequest):
    try:
        return await refresh_access_token(payload.refresh_token)
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

    user = await get_current_user_service(payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ==================================
# 🔄 CHANGE PASSWORD
# ==================================
@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    token: str = Depends(oauth2_scheme),
):
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    await change_user_password(decoded["user_id"], payload)
    return {"message": "Password updated successfully"}


# ==================================
# 📧 REQUEST PASSWORD RESET
# ==================================
@router.post("/password-reset-request")
async def password_reset_request(payload: PasswordResetRequest):
    await request_password_reset(payload.email)
    return {"message": "Password reset email sent (if account exists)"}


# ==================================
# 🔑 CONFIRM PASSWORD RESET
# ==================================
@router.post("/password-reset-confirm")
async def password_reset_confirm(payload: PasswordResetConfirm):
    await confirm_password_reset(payload)
    return {"message": "Password has been reset successfully"}