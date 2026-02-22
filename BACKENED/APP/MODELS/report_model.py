
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.database import report_collection  # Make sure your database.py exports this collection


# ----------------------------
# Pydantic Model for Validation
# ----------------------------
class Report(BaseModel):
    patient_id: str            # MongoDB ObjectId of the patient
    doctor_id: str             # MongoDB ObjectId of the doctor
    appointment_id: Optional[str] = None  # Optional linked appointment
    report_type: str           # e.g., Blood Test, X-ray, MRI
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    file_url: Optional[str] = None  # URL if report is uploaded as file


# ----------------------------
# Helper Functions for CRUD
# ----------------------------

# Create a report
async def create_report(report: Report):
    report_dict = report.dict()
    result = await report_collection.insert_one(report_dict)
    return str(result.inserted_id)


# Get all reports
async def get_all_reports():
    reports = []
    async for doc in report_collection.find():
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        reports.append(doc)
    return reports


# Get report by ID
async def get_report_by_id(report_id: str):
    doc = await report_collection.find_one({"_id": ObjectId(report_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


# Update report by ID
async def update_report(report_id: str, update_data: dict):
    result = await report_collection.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": update_data}
    )
    return result.modified_count


# Delete report by ID
async def delete_report(report_id: str):
    result = await report_collection.delete_one({"_id": ObjectId(report_id)})
    return result.deleted_count