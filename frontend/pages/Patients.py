
from typing import List, Dict, Optional
from bson import ObjectId
from app.database import patient_collection  # Make sure your database.py exports this collection
from app.models.patients_model import Patient

# ----------------------------
# Create Patient
# ----------------------------
async def create_patient(patient: Patient) -> str:
    """
    Insert a new patient into MongoDB.
    """
    patient_dict = patient.dict()
    result = await patient_collection.insert_one(patient_dict)
    return str(result.inserted_id)

# ----------------------------
# Get All Patients
# ----------------------------
async def get_all_patients() -> List[Dict]:
    patients = []
    async for doc in patient_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        patients.append(doc)
    return patients

# ----------------------------
# Get Patient by ID
# ----------------------------
async def get_patient_by_id(patient_id: str) -> Optional[Dict]:
    doc = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ----------------------------
# Update Patient
# ----------------------------
async def update_patient(patient_id: str, update_data: dict) -> int:
    result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_data}
    )
    return result.modified_count

# ----------------------------
# Delete Patient
# ----------------------------
async def delete_patient(patient_id: str) -> int:
    result = await patient_collection.delete_one({"_id": ObjectId(patient_id)})
    return result.deleted_count

# ----------------------------
# Patients Analytics
# ----------------------------
async def patients_by_gender() -> List[Dict]:
    pipeline = [
        {"$group": {"_id": "$gender", "count": {"$sum": 1}}}
    ]
    result = []
    async for doc in patient_collection.aggregate(pipeline):
        result.append({"gender": doc["_id"], "count": doc["count"]})
    return result

async def patients_by_age_group() -> List[Dict]:
    pipeline = [
        {"$bucket": {
            "groupBy": "$age",
            "boundaries": [0, 18, 35, 50, 65, 100],
            "default": "Unknown",
            "output": {"count": {"$sum": 1}}
        }}
    ]
    result = []
    async for doc in patient_collection.aggregate(pipeline):
        result.append(doc)
    return result