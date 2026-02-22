import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List



# =========================
# Load .env from backend/
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


# =========================
# Settings Class
# =========================

class Settings:
    # App
    APP_NAME: str = "Hospital Management AI"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "9f8c1a4d9a3e7f8b4c2d6e5a1b3c9d7f6a2b8c4d1e9f7a6b3c2d4e5f6a7b8c9")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # AI Provider
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost,http://localhost:3000"
    ).split(",")
    ALLOWED_METHODS: List[str] = ["*"]  # allow all HTTP methods

    ALLOWED_HEADERS: List[str] = ["*"]
    
    # API Keys (optional)
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hospital.db")

    MONGO_URI: str = os.getenv("MONGO_URI", "MONGO_URI=mongodb+srv://Cabdb:Cab@clustername.mongodb.net/hospital_db?retryWrites=true&w=majority")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "hospital_db")
settings = Settings()


# =========================
# Safe Warning Instead of Crash
# =========================

if settings.LLM_PROVIDER == "gemini" and not settings.GEMINI_API_KEY:
    print("⚠ WARNING: GEMINI_API_KEY not found. AI features disabled.")

if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
    print("⚠ WARNING: OPENAI_API_KEY not found. AI features disabled.")