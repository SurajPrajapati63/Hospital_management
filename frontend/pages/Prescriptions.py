
from typing import List, Dict, Optional
from bson import ObjectId
from datetime import datetime
from app.database import prescription_collection  # Make sure your database.py exports this collection
from app.models.prescription_model import Prescription

# ----------------------------
# Create Prescription
# ----------------------------
async def create_prescription(prescription: Prescription) -> str:
    """
    Insert a new prescription into MongoDB.
    """
    prescription_dict = prescription.dict()
    if not prescription_dict.get("date"):
        prescription_dict["date"] = datetime.now().strftime("%Y-%m-%d")
    result = await prescription_collection.insert_one(prescription_dict)
    return str(result.inserted_id)

# ----------------------------
# Get All Prescriptions
# ----------------------------
async def get_all_prescriptions() -> List[Dict]:
    prescriptions = []
    async for doc in prescription_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        prescriptions.append(doc)
    return prescriptions

# ----------------------------
# Get Prescription by ID
# ----------------------------
async def get_prescription_by_id(prescription_id: str) -> Optional[Dict]:
    doc = await prescription_collection.find_one({"_id": ObjectId(prescription_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ----------------------------
# Update Prescription
# ----------------------------
async def update_prescription(prescription_id: str, update_data: dict) -> int:
    result = await prescription_collection.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$set": update_data}
    )
    return result.modified_count

# ----------------------------
# Delete Prescription
# ----------------------------
async def delete_prescription(prescription_id: str) -> int:
    result = await prescription_collection.delete_one({"_id": ObjectId(prescription_id)})
    return result.deleted_count

# ----------------------------
# Prescriptions Analytics
# ----------------------------
async def prescriptions_per_doctor() -> List[Dict]:
    pipeline = [
        {"$group": {"_id": "$doctor_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in prescription_collection.aggregate(pipeline):
        result.append({"doctor_id": str(doc["_id"]), "prescriptions": doc["count"]})
    return result

async def prescriptions_per_patient() -> List[Dict]:
    pipeline = [
        {"$group": {"_id": "$patient_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in prescription_collection.aggregate(pipeline):
        result.append({"patient_id": str(doc["_id"]), "prescriptions": doc["count"]})
    return result