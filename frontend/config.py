import os
from dotenv import load_dotenv

# ----------------------------
# Load environment variables from .env
# ----------------------------
load_dotenv()

# ----------------------------
# MongoDB Configuration
# ----------------------------
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hospital_management")

# ----------------------------
# JWT Configuration
# ----------------------------
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "9f8c1a4d9a3e7f8b4c2d6e5a1b3c9d7f6a2b8c4d1e9f7a6b3c2d4e5f6a7b8c9")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# ----------------------------
# Server Configuration
# ----------------------------
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

# ----------------------------
# Other Configurations
# ----------------------------
DEBUG = os.getenv("DEBUG", "True") == "True"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # Can be comma-separated frontend URLs