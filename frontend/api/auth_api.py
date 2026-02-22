import requests
from typing import Optional, Dict
from config import BACKEND_URL, JWT_SECRET_KEY, JWT_ALGORITHM

# ----------------------------
# Backend API Base URL
# ----------------------------
BASE_URL = BACKEND_URL or "http://localhost:8000"

# ----------------------------
# Auth API Client
# ----------------------------

def register_user(email: str, full_name: str, password: str, role: str) -> Optional[Dict]:
    """Register a new user"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": email,
                "full_name": full_name,
                "password": password,
                "role": role
            }
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Registration error: {e}")
        return None


def login_user(email: str, password: str) -> Optional[Dict]:
    """Login user and return tokens"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None


def get_current_user(token: str) -> Optional[Dict]:
    """Get current user details using token"""
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Get current user error: {e}")
        return None


def refresh_token(refresh_token: str) -> Optional[Dict]:
    """Refresh access token"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Token refresh error: {e}")
        return None