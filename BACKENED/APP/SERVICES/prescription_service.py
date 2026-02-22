
from datetime import date, timedelta
from typing import List

from app.schemas.prescription_schema import PrescriptionCreate ,PrescriptionUpdate, PrescriptionResponse, PrescriptionMedicine
from app.database import db
from bson import ObjectId
import datetime


async def create_prescription(payload: PrescriptionCreate):

    issued_date = date.today()
    valid_until = issued_date + timedelta(days=30)

    data = {
        "patient_id": payload.patient_id,
        "doctor_id": payload.doctor_id,
        "appointment_id": payload.appointment_id,
        "diagnosis": payload.diagnosis,
        "medications": [m.dict() for m in payload.medications],
        "notes": payload.notes,
        "issued_date": issued_date,
        "valid_until": valid_until,
        "created_at": datetime.utcnow(),
        "updated_at": None,
    }

    result = db.prescriptions.insert_one(data)

    return PrescriptionResponse(id=str(result.inserted_id), **data)

async def get_prescription_by_id(prescription_id: str):

    prescription = db.prescriptions.find_one({"_id": ObjectId(prescription_id)})

    if not prescription:
        return None

    prescription["id"] = str(prescription["_id"])
    del prescription["_id"]

    return prescription
async def get_patient_prescriptions(prescription_id: str):

    prescription = db.prescriptions.find_one({"_id": ObjectId(prescription_id)})

    if not prescription:
        return None

    prescription["id"] = str(prescription["_id"])
    del prescription["_id"]

    return PrescriptionResponse(**prescription)


async def update_prescription(prescription_id: str, payload: PrescriptionUpdate):

    update_data = {k: v for k, v in payload.dict().items() if v is not None}

    if "medications" in update_data:
        update_data["medications"] = [m.dict() for m in update_data["medications"]]

    update_data["updated_at"] = datetime.utcnow()

    db.prescriptions.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$set": update_data}
    )

    return await get_prescription(prescription_id)


async def delete_prescription(prescription_id: str):
    result = db.prescriptions.delete_one({"_id": ObjectId(prescription_id)})
    return result.deleted_count == 1


async def add_medicine(prescription_id: str, payload: PrescriptionMedicine):

    db.prescriptions.update_one(
        {"_id": ObjectId(prescription_id)},
        {"$push": {"medications": payload.dict()}}
    )

    return await get_prescription(prescription_id)
async def get_doctor_prescriptions(doctor_id: str) -> List[PrescriptionResponse]:

    prescriptions = db.prescriptions.find({"doctor_id": doctor_id})

    result = []

    for prescription in prescriptions:
        prescription["id"] = str(prescription["_id"])
        del prescription["_id"]

        result.append(PrescriptionResponse(**prescription))

    return result