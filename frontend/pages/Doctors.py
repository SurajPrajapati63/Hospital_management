from typing import List, Dict, Optional
from bson import ObjectId
from app.database import doctor_collection  # Make sure your database.py exports this collection
from app.models.doctor_model import Doctor

# ----------------------------
# Create Doctor
# ----------------------------
async def create_doctor(doctor: Doctor) -> str:
    """
    Insert a new doctor into MongoDB.
    """
    doctor_dict = doctor.dict()
    result = await doctor_collection.insert_one(doctor_dict)
    return str(result.inserted_id)

# ----------------------------
# Get All Doctors
# ----------------------------
async def get_all_doctors() -> List[Dict]:
    doctors = []
    async for doc in doctor_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        doctors.append(doc)
    return doctors

# ----------------------------
# Get Doctor by ID
# ----------------------------
async def get_doctor_by_id(doctor_id: str) -> Optional[Dict]:
    doc = await doctor_collection.find_one({"_id": ObjectId(doctor_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ----------------------------
# Update Doctor
# ----------------------------
async def update_doctor(doctor_id: str, update_data: dict) -> int:
    result = await doctor_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": update_data}
    )
    return result.modified_count

# ----------------------------
# Delete Doctor
# ----------------------------
async def delete_doctor(doctor_id: str) -> int:
    result = await doctor_collection.delete_one({"_id": ObjectId(doctor_id)})
    return result.deleted_count