from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.database import doctor_collection  # Make sure your database.py exports this collection


# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Doctor(BaseModel):
    name: str
    specialization: str
    experience: int       # in years
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create a doctor
async def create_doctor(doctor: Doctor):
    doctor_dict = doctor.dict()
    result = await doctor_collection.insert_one(doctor_dict)
    return str(result.inserted_id)


# Get all doctors
async def get_all_doctors():
    doctors = []
    async for doc in doctor_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        doctors.append(doc)
    return doctors


# Get doctor by ID
async def get_doctor_by_id(doctor_id: str):
    doc = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update doctor by ID
async def update_doctor(doctor_id: str, update_data: dict):
    result = await doctor_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete doctor by ID
async def delete_doctor(doctor_id: str):
    result = await doctor_collection.delete_one({"_id": ObjectId(doctor_id)})
    return result.deleted_count