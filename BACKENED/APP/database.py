from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Optional
import certifi
from app.config import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)

# ==========================================
# 🌐 CREATE MONGO CLIENT
# ==========================================

client: Optional[MongoClient] = None
db = None


def connect_to_database():
    global client, db

    try:
        client = MongoClient(settings.MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where())
        db = client[settings.MONGO_DB_NAME]

        # Test connection
        client.admin.command("ping")

        logger.info(" MongoDB connected successfully")

        create_indexes()

    except ConnectionFailure as e:
        logger.error(f" MongoDB connection failed: {e}")
        raise e


def close_database_connection():
    global client

    if client:
        client.close()
        logger.info(" MongoDB connection closed")


# ==========================================
# 📊 CREATE INDEXES (IMPORTANT FOR PROD)
# ==========================================

def create_indexes():
    """
    Create important indexes for performance.
    """

    # Patients
    db.patients.create_index("email", unique=True)
    db.patients.create_index("full_name")

    # Doctors
    db.doctors.create_index("email", unique=True)
    db.doctors.create_index("specialization")
    db.doctors.create_index("department")

    # Appointments
    db.appointments.create_index("doctor_id")
    db.appointments.create_index("patient_id")
    db.appointments.create_index("appointment_date")

    # Billing
    db.billing.create_index("patient_id")
    db.billing.create_index("payment_status")
    db.billing.create_index("created_at")

    # Users
    db.users.create_index("email", unique=True)

    logger.info(" MongoDB indexes created successfully")


# ==========================================
# 🩺 HEALTH CHECK
# ==========================================

def check_database_health() -> bool:
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False