from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.database import patient_collection  # Make sure your database.py exports this collection


# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Patient(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create a patient
async def create_patient(patient: Patient):
    patient_dict = patient.dict()
    result = await patient_collection.insert_one(patient_dict)
    return str(result.inserted_id)


# Get all patients
async def get_all_patients():
    patients = []
    async for doc in patient_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        patients.append(doc)
    return patients


# Get patient by ID
async def get_patient_by_id(patient_id: str):
    doc = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update patient by ID
async def update_patient(patient_id: str, update_data: dict):
    result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete patient by ID
async def delete_patient(patient_id: str):
    result = await patient_collection.delete_one({"_id": ObjectId(patient_id)})
    return result.deleted_count