from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.database import connect_db, close_db
from app.components.Login import decode_access_token
from app.routers import (
    patients_api,
    doctors_api,
    appointments_api,
    prescriptions_api,
    billing_api,
    analytics_api,
    ai_api,
    chat_api,
    auth_api
)

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(
    title="Hospital Management System",
    description="Complete backend API for hospital management with AI assistant, analytics, and JWT authentication",
    version="1.0.0"
)

# ----------------------------
# CORS Middleware
# ----------------------------
origins = ["*"]  # You can restrict to frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------------
# Startup and Shutdown Events
# ----------------------------
@app.on_event("startup")
async def startup_db():
    await connect_db()
    print("MongoDB connected!")

@app.on_event("shutdown")
async def shutdown_db():
    await close_db()
    print("MongoDB disconnected!")

# ----------------------------
# JWT Dependency
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(auth_api.router, prefix="/auth", tags=["Authentication"])
app.include_router(patients_api.router, prefix="/patients", tags=["Patients"])
app.include_router(doctors_api.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments_api.router, prefix="/appointments", tags=["Appointments"])
app.include_router(prescriptions_api.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(billing_api.router, prefix="/billing", tags=["Billing"])
app.include_router(analytics_api.router, prefix="/analytics", tags=["Analytics"])
app.include_router(ai_api.router, prefix="/ai", tags=["AI Assistant"])
app.include_router(chat_api.router, prefix="/chat", tags=["Chat"])

# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to Hospital Management System API"}