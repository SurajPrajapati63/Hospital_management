from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.database import user_collection  # Make sure your database.py exports this collection
from app.models.auth_model import User

# ----------------------------
# Password Hashing
# ----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ----------------------------
# JWT Configuration
# ----------------------------
SECRET_KEY = "your-secret-key"  # Replace with strong secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------------------
# User Authentication
# ----------------------------
async def authenticate_user(username: str, password: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }

# ----------------------------
# Create New User
# ----------------------------
async def create_user(user: User) -> str:
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    
    result = await user_collection.insert_one(user_dict)
    return str(result.inserted_id)