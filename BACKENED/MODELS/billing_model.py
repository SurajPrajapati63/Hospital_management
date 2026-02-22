
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.database import database  # make sure database.py exports a Motor client
from app.database import billing_collection  # Collection for billing

# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Billing(BaseModel):
    patient_id: str           # MongoDB ObjectId of the patient as string
    appointment_id: Optional[str] = None  # Optional linked appointment
    doctor_id: str            # MongoDB ObjectId of the doctor
    services: list            # List of services or treatments
    total_amount: float
    status: Optional[str] = "Unpaid"  # Paid / Unpaid
    payment_method: Optional[str] = None  # Cash / Card / Online
    billing_date: Optional[str] = None  # YYYY-MM-DD


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create a billing record
async def create_billing(billing: Billing):
    billing_dict = billing.dict()
    result = await billing_collection.insert_one(billing_dict)
    return str(result.inserted_id)


# Get all billing records
async def get_all_billings():
    billings = []
    async for doc in billing_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        billings.append(doc)
    return billings


# Get billing by ID
async def get_billing_by_id(billing_id: str):
    doc = await billing_collection.find_one({"_id": ObjectId(billing_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update billing by ID
async def update_billing(billing_id: str, update_data: dict):
    result = await billing_collection.update_one(
        {"_id": ObjectId(billing_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete billing by ID
async def delete_billing(billing_id: str):
    result = await billing_collection.delete_one({"_id": ObjectId(billing_id)})
    return result.deleted_count