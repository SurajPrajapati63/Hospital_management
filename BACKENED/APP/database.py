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

# Collection references (exported for use in models/services)
patients = None
doctors = None
appointments = None
prescriptions = None
billing = None
users = None
reports = None
ai_conversations = None


def connect_to_database():
    global client, db, patients, doctors, appointments, prescriptions, billing, users, reports, ai_conversations

    try:
        # Check if using local MongoDB
        is_local_mongo = "localhost" in settings.MONGO_URI or "127.0.0.1" in settings.MONGO_URI
        
        client = MongoClient(
            settings.MONGO_URI,
            tls=not is_local_mongo,  # TLS only for cloud MongoDB
            tlsCAFile=certifi.where() if not is_local_mongo else None,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000
        )
        db = client[settings.MONGO_DB_NAME]

        # Initialize collection references
        patients = db.patients
        doctors = db.doctors
        appointments = db.appointments
        prescriptions = db.prescriptions
        billing = db.billing
        users = db.users
        reports = db.reports
        ai_conversations = db.ai_conversations

        # Test connection
        client.admin.command("ping")

        logger.info("✅ MongoDB connected successfully")
        create_indexes()

    except ConnectionFailure as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.warning("⚠️  Application starting without database. Please ensure MongoDB is running on localhost:27017")
        # Don't raise - allow app to start anyway for development
        client = None
        db = None
    except Exception as e:
        logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
        logger.warning("⚠️  Application starting without database. Please ensure MongoDB is running.")
        client = None
        db = None


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