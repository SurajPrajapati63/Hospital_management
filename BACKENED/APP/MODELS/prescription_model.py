
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from app.database import prescription_collection  # Make sure your database.py exports this collection


# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Prescription(BaseModel):
    patient_id: str           # MongoDB ObjectId of the patient
    doctor_id: str            # MongoDB ObjectId of the doctor
    appointment_id: Optional[str] = None  # Optional linked appointment
    medicines: List[str]      # List of medicine names
    dosage: List[str]         # Corresponding dosages
    instructions: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    notes: Optional[str] = None


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create a prescription
async def create_prescription(prescription: Prescription):
    prescription_dict = prescription.dict()
    result = await prescription_collection.insert_one(prescription_dict)
    return str(result.inserted_id)


# Get all prescriptions
async def get_all_prescriptions():
    prescriptions = []
    async for doc in prescription_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        prescriptions.append(doc)
    return prescriptions


# Get prescription by ID
async def get_prescription_by_id(prescription_id: str):
    doc = await prescription_collection.find_one({"_id": ObjectId(prescription_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update prescription by ID
async def update_prescription(prescription_id: str, update_data: dict):
    result = await prescription_collection.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete prescription by ID
async def delete_prescription(prescription_id: str):
    result = await prescription_collection.delete_one({"_id": ObjectId(prescription_id)})
    return result.deleted_count