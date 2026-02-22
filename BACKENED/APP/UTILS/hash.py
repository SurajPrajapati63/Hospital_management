from passlib.context import CryptContext


# ==========================================
# 🔐 Password Hashing Configuration
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================
# 🔑 HASH PASSWORD
# ==========================================
def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    """
    return pwd_context.hash(password)


# ==========================================
# ✅ VERIFY PASSWORD
# ==========================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if plain password matches hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# 🔄 OPTIONAL: REHASH CHECK
# ==========================================
def needs_rehash(hashed_password: str) -> bool:
    """
    Check if password needs rehash (e.g., algorithm upgrade).
    """
    return pwd_context.needs_update(hashed_password)