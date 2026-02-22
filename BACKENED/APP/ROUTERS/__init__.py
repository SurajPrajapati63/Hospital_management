"""
Routers Module
Exports all API routers
"""

from . import auth
from . import patients
from . import doctors
from . import appointments
from . import billing
from . import prescriptions
from . import ai_routes
from . import analytics

__all__ = [
    "auth",
    "patients",
    "doctors",
    "appointments",
    "billing",
    "prescriptions",
    "ai_routes",
    "analytics",
]
