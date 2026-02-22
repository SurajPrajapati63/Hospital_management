import os
from pathlib import Path
from dotenv import load_dotenv


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

    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Optional future expansion
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")

    # Database (optional, safe default)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hospital.db")


settings = Settings()


# =========================
# Basic Safety Check
# =========================

if settings.LLM_PROVIDER == "gemini" and not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")