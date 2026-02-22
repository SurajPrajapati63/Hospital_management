from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.database import db
from app.schemas.doctor_schema import (
    DoctorCreate,
    DoctorUpdate,
    DoctorFilter,
    DoctorAvailability,
    DoctorStatus,
)


# ==========================================
# 👨‍⚕️ CREATE DOCTOR
# ==========================================
def create_doctor(payload: DoctorCreate):
    """Create a new doctor"""
    doctor_data = payload.dict()

    doctor_data.update({
        "status": DoctorStatus.active,
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "availability": []
    })

    result = db.doctors.insert_one(doctor_data)
    doctor_data["id"] = str(result.inserted_id)

    return doctor_data


# ==========================================
# 📄 GET DOCTOR BY ID
# ==========================================
def get_doctor_by_id(doctor_id: str):
    """Get doctor by ID"""
    doctor = db.doctors.find_one({"_id": ObjectId(doctor_id)})

    if doctor:
        doctor["id"] = str(doctor["_id"])

    return doctor


# ==========================================
# 📋 GET ALL DOCTORS (FILTERABLE)
# ==========================================
def get_all_doctors(filters: DoctorFilter):
    """Get all doctors with optional filters"""
    query = {}

    if filters.specialization:
        query["specialization"] = filters.specialization

    if filters.department:
        query["department"] = filters.department

    if filters.consultation_mode:
        query["consultation_mode"] = filters.consultation_mode

    if filters.status:
        query["status"] = filters.status

    if filters.min_experience:
        query["experience_years"] = {"$gte": filters.min_experience}

    if filters.max_fee:
        query["consultation_fee"] = {"$lte": filters.max_fee}

    doctors = list(db.doctors.find(query))

    for doctor in doctors:
        doctor["id"] = str(doctor["_id"])

    return doctors


# ==========================================
# ✏ UPDATE DOCTOR
# ==========================================
def update_doctor(doctor_id: str, payload: DoctorUpdate):
    """Update doctor information"""
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return None

    return get_doctor_by_id(doctor_id)


# ==========================================
# 🗑 DELETE DOCTOR
# ==========================================
def delete_doctor(doctor_id: str):
    """Delete doctor"""
    result = db.doctors.delete_one({"_id": ObjectId(doctor_id)})
    return result.deleted_count > 0


# ==========================================
# 🟢 UPDATE DOCTOR STATUS
# ==========================================
def update_doctor_status(doctor_id: str, status: DoctorStatus):
    """Update doctor status (active, inactive, on_leave)"""
    result = db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {
            "status": status,
            "updated_at": datetime.utcnow()
        }}
    )

    if result.modified_count == 0:
        return None

    return get_doctor_by_id(doctor_id)


# ==========================================
# ⏰ ADD DOCTOR AVAILABILITY
# ==========================================
def add_doctor_availability(doctor_id: str, availability: DoctorAvailability):
    """Add availability slot for doctor"""
    result = db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$push": {
            "availability": availability.dict()
        }}
    )

    if result.modified_count == 0:
        return None

    return get_doctor_by_id(doctor_id)


# ==========================================
# 📅 GET DOCTOR AVAILABILITY
# ==========================================
def get_doctor_availability(doctor_id: str):
    """Get doctor's availability schedule"""
    doctor = db.doctors.find_one({"_id": ObjectId(doctor_id)})

    if not doctor:
        return None

    return doctor.get("availability", [])


# ==========================================
# 📊 DOCTOR STATISTICS
# ==========================================
def get_doctor_statistics(doctor_id: str):
    """Get doctor's appointment and rating statistics"""
    total_appointments = db.appointments.count_documents({
        "doctor_id": doctor_id
    })

    completed_appointments = db.appointments.count_documents({
        "doctor_id": doctor_id,
        "status": "completed"
    })

    cancelled_appointments = db.appointments.count_documents({
        "doctor_id": doctor_id,
        "status": "cancelled"
    })

    return {
        "doctor_id": doctor_id,
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "average_rating": 4.5  # Placeholder - would need ratings collection
    }
