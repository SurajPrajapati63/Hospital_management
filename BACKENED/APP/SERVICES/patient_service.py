from datetime import datetime, date
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.database import db
from app.schemas.patient_schema import (
    PatientCreate,
    PatientUpdate,
    PatientFilter,
    MedicalHistory,
)


# ==========================================
# 👤 CREATE PATIENT
# ==========================================
async def create_patient(payload: PatientCreate):

    patient_data = payload.dict()

    patient_data.update({
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "medical_history": {}
    })

    result = db.patients.insert_one(patient_data)
    patient_data["id"] = str(result.inserted_id)

    return patient_data


# ==========================================
# 📄 GET PATIENT BY ID
# ==========================================
async def get_patient_by_id(patient_id: str):

    patient = db.patients.find_one({"_id": ObjectId(patient_id)})

    if patient:
        patient["id"] = str(patient["_id"])

    return patient


# ==========================================
# 📋 GET ALL PATIENTS (FILTERABLE)
# ==========================================
async def get_all_patients(filters: PatientFilter):

    query = {}

    if filters.gender:
        query["gender"] = filters.gender

    if filters.blood_group:
        query["blood_group"] = filters.blood_group

    # Age filtering
    today = date.today()

    if filters.min_age:
        max_dob = date(today.year - filters.min_age, today.month, today.day)
        query["date_of_birth"] = {"$lte": max_dob}

    if filters.max_age:
        min_dob = date(today.year - filters.max_age, today.month, today.day)
        query.setdefault("date_of_birth", {})
        query["date_of_birth"]["$gte"] = min_dob

    if filters.chronic_disease:
        query["medical_history.chronic_diseases"] = filters.chronic_disease

    patients = list(db.patients.find(query))

    for patient in patients:
        patient["id"] = str(patient["_id"])

    return patients


# ==========================================
# ✏ UPDATE PATIENT
# ==========================================
async def update_patient(patient_id: str, payload: PatientUpdate):

    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = db.patients.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return None

    return await get_patient_by_id(patient_id)


# ==========================================
# 🗑 DELETE PATIENT
# ==========================================
async def delete_patient(patient_id: str):

    result = db.patients.delete_one({"_id": ObjectId(patient_id)})
    return result.deleted_count > 0


# ==========================================
# 🩺 UPDATE MEDICAL HISTORY
# ==========================================
async def update_medical_history(patient_id: str, payload: MedicalHistory):

    history_data = payload.dict(exclude_none=True)

    result = db.patients.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"medical_history": history_data}}
    )

    if result.modified_count == 0:
        return None

    return await get_patient_by_id(patient_id)


# ==========================================
# 📊 PATIENT STATISTICS
# ==========================================
async def get_patient_stats(patient_id: str):

    total_appointments = db.appointments.count_documents({
        "patient_id": patient_id
    })

    completed_appointments = db.appointments.count_documents({
        "patient_id": patient_id,
        "status": "completed"
    })

    cancelled_appointments = db.appointments.count_documents({
        "patient_id": patient_id,
        "status": "cancelled"
    })

    total_bills = sum(
        bill.get("total_amount", 0)
        for bill in db.billing.find({"patient_id": patient_id})
    )

    outstanding_balance = sum(
        bill.get("total_amount", 0)
        for bill in db.billing.find({
            "patient_id": patient_id,
            "payment_status": "pending"
        })
    )

    return {
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "total_bills": total_bills,
        "outstanding_balance": outstanding_balance,
    }


# ==========================================
# 🤖 GET PATIENT AI CONTEXT
# ==========================================
async def get_patient_ai_context(patient_id: str):

    patient = await get_patient_by_id(patient_id)

    if not patient:
        return None

    age = date.today().year - patient["date_of_birth"].year

    return {
        "patient_id": patient_id,
        "age": age,
        "gender": patient.get("gender"),
        "blood_group": patient.get("blood_group"),
        "chronic_conditions": patient.get("medical_history", {}).get("chronic_diseases"),
        "allergies": patient.get("medical_history", {}).get("allergies"),
        "recent_reports_summary": "No recent reports available"
    }