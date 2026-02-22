from typing import Optional, List, Dict
from bson import ObjectId
from datetime import datetime
from app.database import appointment_collection  # Make sure your database.py exports this collection
from app.models.appointment_model import Appointment

# ----------------------------
# Create Appointment
# ----------------------------
async def create_appointment(appointment: Appointment) -> str:
    """
    Insert a new appointment into MongoDB.
    """
    appointment_dict = appointment.dict()
    result = await appointment_collection.insert_one(appointment_dict)
    return str(result.inserted_id)

# ----------------------------
# Get All Appointments
# ----------------------------
async def get_all_appointments() -> List[Dict]:
    appointments = []
    async for doc in appointment_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        appointments.append(doc)
    return appointments

# ----------------------------
# Get Appointment by ID
# ----------------------------
async def get_appointment_by_id(appointment_id: str) -> Optional[Dict]:
    doc = await appointment_collection.find_one({"_id": ObjectId(appointment_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ----------------------------
# Update Appointment
# ----------------------------
async def update_appointment(appointment_id: str, update_data: dict) -> int:
    result = await appointment_collection.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_data}
    )
    return result.modified_count

# ----------------------------
# Delete Appointment
# ----------------------------
async def delete_appointment(appointment_id: str) -> int:
    result = await appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
    return result.deleted_count

# ----------------------------
# Appointments Analytics
# ----------------------------
async def appointments_per_doctor() -> List[Dict]:
    pipeline = [
        {"$group": {"_id": "$doctor_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in appointment_collection.aggregate(pipeline):
        result.append({"doctor_id": str(doc["_id"]), "appointments": doc["count"]})
    return result

async def appointments_per_patient() -> List[Dict]:
    pipeline = [
        {"$group": {"_id": "$patient_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in appointment_collection.aggregate(pipeline):
        result.append({"patient_id": str(doc["_id"]), "appointments": doc["count"]})
    return result

# ----------------------------
# Upcoming Appointments
# ----------------------------
async def upcoming_appointments() -> List[Dict]:
    today = datetime.now().strftime("%Y-%m-%d")
    appointments = []
    async for doc in appointment_collection.find({"appointment_date": {"$gte": today}}):
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        appointments.append(doc)
    return appointments