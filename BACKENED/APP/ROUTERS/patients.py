from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from app.schemas.patient_schema import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientPublicView,
    PatientFilter,
    PatientStats,
    MedicalHistory,
    PatientAIContext,
)

from app.services.patient_service import (
    create_patient,
    get_patient_by_id,
    get_all_patients,
    update_patient,
    delete_patient,
    get_patient_stats,
    update_medical_history,
    get_patient_ai_context,
)

router = APIRouter(prefix="/patients", tags=["Patients"])


# ==================================
# 👤 CREATE PATIENT
# ==================================
@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: PatientCreate):
    try:
        return await create_patient(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 📋 GET ALL PATIENTS (WITH FILTER)
# ==================================
@router.get("/", response_model=List[PatientPublicView])
async def get_all(
    gender: Optional[str] = None,
    blood_group: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    chronic_disease: Optional[str] = None,
):
    try:
        filters = PatientFilter(
            gender=gender,
            blood_group=blood_group,
            min_age=min_age,
            max_age=max_age,
            chronic_disease=chronic_disease,
        )
        return await get_all_patients(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================
# 📄 GET PATIENT BY ID
# ==================================
@router.get("/{patient_id}", response_model=PatientResponse)
async def get_by_id(patient_id: int):
    patient = await get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ==================================
# ✏ UPDATE PATIENT
# ==================================
@router.put("/{patient_id}", response_model=PatientResponse)
async def update(patient_id: int, payload: PatientUpdate):
    updated = await update_patient(patient_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated


# ==================================
# 🗑 DELETE PATIENT
# ==================================
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(patient_id: int):
    deleted = await delete_patient(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None


# ==================================
# 📊 PATIENT STATISTICS
# ==================================
@router.get("/{patient_id}/stats", response_model=PatientStats)
async def stats(patient_id: int):
    return await get_patient_stats(patient_id)


# ==================================
# 🩺 UPDATE MEDICAL HISTORY
# ==================================
@router.put("/{patient_id}/medical-history", response_model=PatientResponse)
async def update_history(patient_id: int, payload: MedicalHistory):
    updated = await update_medical_history(patient_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated


# ==================================
# 🤖 PATIENT AI CONTEXT (For GenAI)
# ==================================
@router.get("/{patient_id}/ai-context", response_model=PatientAIContext)
async def ai_context(patient_id: int):
    context = await get_patient_ai_context(patient_id)
    if not context:
        raise HTTPException(status_code=404, detail="Patient not found")
    return context