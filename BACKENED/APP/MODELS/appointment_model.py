
from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from bson import ObjectId
from app.database import appointment_collection

# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Appointment(BaseModel):
    patient_id: str       # MongoDB ObjectId of patient as string
    doctor_id: str        # MongoDB ObjectId of doctor as string
    appointment_date: str # YYYY-MM-DD
    appointment_time: str # HH:MM
    reason: Optional[str] = None
    status: Optional[str] = "Scheduled"


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create an appointment
async def create_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    result = await appointment_collection.insert_one(appointment_dict)
    return str(result.inserted_id)


# Get all appointments
async def get_all_appointments():
    appointments = []
    async for doc in appointment_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        appointments.append(doc)
    return appointments


# Get appointment by ID
async def get_appointment_by_id(appointment_id: str):
    doc = await appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update appointment by ID
async def update_appointment(appointment_id: str, update_data: dict):
    result = await appointment_collection.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete appointment by ID
async def delete_appointment(appointment_id: str):
    result = await appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
    return result.deleted_count