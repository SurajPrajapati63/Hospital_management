
from app.database import (
    patient_collection,
    doctor_collection,
    appointment_collection,
    prescription_collection,
    billing_collection,
    report_collection
)
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any

# ----------------------------
# Basic Analytics Functions
# ----------------------------

# Total counts
async def total_patients() -> int:
    return await patient_collection.count_documents({})

async def total_doctors() -> int:
    return await doctor_collection.count_documents({})

async def total_appointments() -> int:
    return await appointment_collection.count_documents({})

async def total_prescriptions() -> int:
    return await prescription_collection.count_documents({})

async def total_billings() -> int:
    return await billing_collection.count_documents({})

async def total_reports() -> int:
    return await report_collection.count_documents({})

# ----------------------------
# Appointments Analytics
# ----------------------------
async def appointments_per_doctor() -> list:
    pipeline = [
        {"$group": {"_id": "$doctor_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in appointment_collection.aggregate(pipeline):
        result.append({"doctor_id": str(doc["_id"]), "appointments": doc["count"]})
    return result

async def appointments_per_patient() -> list:
    pipeline = [
        {"$group": {"_id": "$patient_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in appointment_collection.aggregate(pipeline):
        result.append({"patient_id": str(doc["_id"]), "appointments": doc["count"]})
    return result

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

async def revenue_per_doctor() -> list:
    pipeline = [
        {"$match": {"status": "Paid"}},
        {"$group": {"_id": "$doctor_id", "total": {"$sum": "$total_amount"}}},
        {"$sort": {"total": -1}}
    ]
    result = []
    async for doc in billing_collection.aggregate(pipeline):
        result.append({"doctor_id": str(doc["_id"]), "revenue": doc["total"]})
    return result

# ----------------------------
# Patient Analytics
# ----------------------------
async def patients_by_gender() -> list:
    pipeline = [
        {"$group": {"_id": "$gender", "count": {"$sum": 1}}}
    ]
    result = []
    async for doc in patient_collection.aggregate(pipeline):
        result.append({"gender": doc["_id"], "count": doc["count"]})
    return result

async def patients_by_age_group() -> list:
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

# ----------------------------
# Reports Analytics
# ----------------------------
async def reports_per_type() -> list:
    pipeline = [
        {"$group": {"_id": "$report_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = []
    async for doc in report_collection.aggregate(pipeline):
        result.append({"report_type": doc["_id"], "count": doc["count"]})
    return result

# ----------------------------
# Full Dashboard Analytics
# ----------------------------
async def dashboard_summary() -> Dict[str, Any]:
    summary = {
        "total_patients": await total_patients(),
        "total_doctors": await total_doctors(),
        "total_appointments": await total_appointments(),
        "total_prescriptions": await total_prescriptions(),
        "total_billings": await total_billings(),
        "total_revenue": await total_revenue(),
    }
    return summary