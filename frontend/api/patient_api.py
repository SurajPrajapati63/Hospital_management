from fastapi import APIRouter, HTTPException
from typing import List
from app.models.patient_model import (
    Patient,
    create_patient,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient
)

router = APIRouter()

# ----------------------------
# Create Patient
# ----------------------------
@router.post("/patients", response_model=dict)
async def add_patient(patient: Patient):
    patient_id = await create_patient(patient)
    return {"id": patient_id, "message": "Patient created successfully"}


# ----------------------------
# Get All Patients
# ----------------------------
@router.get("/patients", response_model=List[dict])
async def list_patients():
    return await get_all_patients()


# ----------------------------
# Get Patient by ID
# ----------------------------
@router.get("/patients/{patient_id}", response_model=dict)
async def get_patient(patient_id: str):
    patient = await get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ----------------------------
# Update Patient
# ----------------------------
@router.put("/patients/{patient_id}", response_model=dict)
async def update_patient_api(patient_id: str, update_data: dict):
    updated_count = await update_patient(patient_id, update_data)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found or no changes made")
    return {"message": "Patient updated successfully"}


# ----------------------------
# Delete Patient
# ----------------------------
@router.delete("/patients/{patient_id}", response_model=dict)
async def delete_patient_api(patient_id: str):
    deleted_count = await delete_patient(patient_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}