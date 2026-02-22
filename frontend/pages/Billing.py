from typing import List, Dict, Optional
from bson import ObjectId
from datetime import datetime
from app.database import billing_collection  # Make sure your database.py exports this collection
from app.models.billing_model import Billing

# ----------------------------
# Create Billing Record
# ----------------------------
async def create_billing(billing: Billing) -> str:
    """
    Insert a new billing record into MongoDB.
    """
    billing_dict = billing.dict()
    # Automatically set billing date if not provided
    if not billing_dict.get("billing_date"):
        billing_dict["billing_date"] = datetime.now().strftime("%Y-%m-%d")
    result = await billing_collection.insert_one(billing_dict)
    return str(result.inserted_id)

# ----------------------------
# Get All Billing Records
# ----------------------------
async def get_all_billings() -> List[Dict]:
    billings = []
    async for doc in billing_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        billings.append(doc)
    return billings

# ----------------------------
# Get Billing Record by ID
# ----------------------------
async def get_billing_by_id(billing_id: str) -> Optional[Dict]:
    doc = await billing_collection.find_one({"_id": ObjectId(billing_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# ----------------------------
# Update Billing Record
# ----------------------------
async def update_billing(billing_id: str, update_data: dict) -> int:
    result = await billing_collection.update_one(
        {"_id": ObjectId(billing_id)},
        {"$set": update_data}
    )
    return result.modified_count

# ----------------------------
# Delete Billing Record
# ----------------------------
async def delete_billing(billing_id: str) -> int:
    result = await billing_collection.delete_one({"_id": ObjectId(billing_id)})
    return result.deleted_count

# ----------------------------
# Billing Analytics
# ----------------------------
async def total_revenue() -> float:
    pipeline = [
        {"$match": {"status": "Paid"}},
        {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
    ]
    result = await billing_collection.aggregate(pipeline).to_list(length=1)
    if result:
        return result[0]["total"]
    return 0.0

async def revenue_per_doctor() -> List[Dict]:
    pipeline = [
        {"$match": {"status": "Paid"}},
        {"$group": {"_id": "$doctor_id", "total_revenue": {"$sum": "$total_amount"}}},
        {"$sort": {"total_revenue": -1}}
    ]
    result = []
    async for doc in billing_collection.aggregate(pipeline):
        result.append({"doctor_id": str(doc["_id"]), "revenue": doc["total_revenue"]})
    return result

# ----------------------------
# Pending Payments
# ----------------------------
async def pending_payments() -> List[Dict]:
    billings = []
    async for doc in billing_collection.find({"status": "Unpaid"}):
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        billings.append(doc)
    return billings