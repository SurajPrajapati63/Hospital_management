from datetime import date, timedelta, datetime as dt
from typing import List, Optional

from app.schemas.prescription_schema import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionMedicine
)
from app.database import db
from bson import ObjectId


# ==========================================
# 📝 CREATE PRESCRIPTION
# ==========================================
def create_prescription(payload: PrescriptionCreate):
    """Create a new prescription"""
    issued_date = date.today()
    valid_until = issued_date + timedelta(days=30)

    data = {
        "patient_id": payload.patient_id,
        "doctor_id": payload.doctor_id,
        "appointment_id": payload.appointment_id,
        "diagnosis": payload.diagnosis,
        "medications": [m.dict() for m in payload.medications],
        "notes": payload.notes,
        "issued_date": issued_date,
        "valid_until": valid_until,
        "created_at": dt.utcnow(),
        "updated_at": None,
    }

    result = db.prescriptions.insert_one(data)
    data["id"] = str(result.inserted_id)

    return data


# ==========================================
# 📄 GET PRESCRIPTION BY ID
# ==========================================
def get_prescription_by_id(prescription_id: str):
    """Get prescription by ID"""
    prescription = db.prescriptions.find_one({"_id": ObjectId(prescription_id)})

    if not prescription:
        return None

    prescription["id"] = str(prescription["_id"])

    return prescription


# ==========================================
# 👤 GET PATIENT PRESCRIPTIONS
# ==========================================
def get_patient_prescriptions(patient_id: str) -> List:
    """Get all prescriptions for a patient"""
    prescriptions = list(db.prescriptions.find({"patient_id": patient_id}))

    for prescription in prescriptions:
        prescription["id"] = str(prescription["_id"])

    return prescriptions


# ==========================================
# 👨‍⚕️ GET DOCTOR PRESCRIPTIONS
# ==========================================
def get_doctor_prescriptions(doctor_id: str) -> List:
    """Get all prescriptions created by a doctor"""
    prescriptions = list(db.prescriptions.find({"doctor_id": doctor_id}))

    for prescription in prescriptions:
        prescription["id"] = str(prescription["_id"])

    return prescriptions


# ==========================================
# ✏ UPDATE PRESCRIPTION
# ==========================================
def update_prescription(prescription_id: str, payload: PrescriptionUpdate):
    """Update prescription"""
    update_data = {k: v for k, v in payload.dict().items() if v is not None}

    if "medications" in update_data:
        update_data["medications"] = [m.dict() for m in update_data["medications"]]

    update_data["updated_at"] = dt.utcnow()

    result = db.prescriptions.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return None

    return get_prescription_by_id(prescription_id)


# ==========================================
# 🗑 DELETE PRESCRIPTION
# ==========================================
def delete_prescription(prescription_id: str):
    """Delete prescription"""
    result = db.prescriptions.delete_one({"_id": ObjectId(prescription_id)})
    return result.deleted_count == 1


# ==========================================
# ➕ ADD MEDICINE TO PRESCRIPTION
# ==========================================
def add_medicine_to_prescription(prescription_id: str, payload: PrescriptionMedicine):
    """Add medicine to prescription"""
    result = db.prescriptions.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$push": {"medications": payload.dict()}}
    )

    if result.modified_count == 0:
        return None

    return get_prescription_by_id(prescription_id)