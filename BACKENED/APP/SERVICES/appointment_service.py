from datetime import datetime
from typing import List, Optional

from app.database import db
from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentFilter,
)


# ==========================================
# 📌 CREATE APPOINTMENT
# ==========================================
def create_appointment(payload: AppointmentCreate):

    # Check doctor availability (basic example)
    conflict = db.appointments.find_one({
        "doctor_id": payload.doctor_id,
        "appointment_date": payload.appointment_date,
        "status": {"$in": ["scheduled", "confirmed"]}
    })

    if conflict:
        raise Exception("Doctor already booked for this time")

    appointment_data = payload.dict()
    appointment_data.update({
        "status": "scheduled",
        "payment_status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": None
    })

    result = db.appointments.insert_one(appointment_data)
    appointment_data["id"] = str(result.inserted_id)

    return appointment_data


# ==========================================
# 📌 GET APPOINTMENT BY ID
# ==========================================
def get_appointment_by_id(appointment_id: int):
    return db.appointments.find_one({"id": appointment_id})


# ==========================================
# 📌 GET ALL APPOINTMENTS WITH FILTER
# ==========================================
def get_all_appointments(filters: AppointmentFilter):

    query = {}

    if filters.doctor_id:
        query["doctor_id"] = filters.doctor_id

    if filters.patient_id:
        query["patient_id"] = filters.patient_id

    if filters.status:
        query["status"] = filters.status

    if filters.start_date and filters.end_date:
        query["appointment_date"] = {
            "$gte": filters.start_date,
            "$lte": filters.end_date
        }

    return list(db.appointments.find(query))


# ==========================================
# ✏ UPDATE APPOINTMENT
# ==========================================
def update_appointment(appointment_id: int, payload: AppointmentUpdate):

    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = db.appointments.update_one(
        {"id": appointment_id},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return None

    return db.appointments.find_one({"id": appointment_id})


# ==========================================
# ❌ CANCEL APPOINTMENT
# ==========================================
def cancel_appointment(appointment_id: int):

    result = db.appointments.update_one(
        {"id": appointment_id},
        {"$set": {
            "status": "cancelled",
            "updated_at": datetime.utcnow()
        }}
    )

    if result.modified_count == 0:
        return None

    return db.appointments.find_one({"id": appointment_id})


# ==========================================
# 🗑 DELETE APPOINTMENT
# ==========================================
def delete_appointment(appointment_id: int):

    result = db.appointments.delete_one({"id": appointment_id})
    return result.deleted_count > 0


# ==========================================
# 👤 GET PATIENT APPOINTMENTS
# ==========================================
def get_patient_appointments(patient_id: int):

    return list(db.appointments.find({"patient_id": patient_id}))


# ==========================================
# 👨‍⚕️ GET DOCTOR APPOINTMENTS
# ==========================================
def get_doctor_appointments(doctor_id: int):

    return list(db.appointments.find({"doctor_id": doctor_id}))