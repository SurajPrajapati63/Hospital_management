from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from app.schemas.doctor_schema import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    DoctorPublicView,
    DoctorFilter,
    DoctorAvailability,
    DoctorStats,
    DoctorStatus,
)

from app.services.doctor_service import (
    create_doctor,
    get_doctor_by_id,
    get_all_doctors,
    update_doctor,
    delete_doctor,
    update_doctor_status,
    add_doctor_availability,
    get_doctor_availability,
    get_doctor_statistics,
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# ==================================
# 👨‍⚕️ CREATE DOCTOR
# ==================================
@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: DoctorCreate):
    try:
        return create_doctor(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 📋 GET ALL DOCTORS (WITH FILTER)
# ==================================
@router.get("/", response_model=List[DoctorPublicView])
async def get_all(
    specialization: Optional[str] = None,
    department: Optional[str] = None,
    consultation_mode: Optional[str] = None,
    status: Optional[str] = None,
    min_experience: Optional[int] = None,
    max_fee: Optional[float] = None,
):
    try:
        filters = DoctorFilter(
            specialization=specialization,
            department=department,
            consultation_mode=consultation_mode,
            status=status,
            min_experience=min_experience,
            max_fee=max_fee,
        )
        return get_all_doctors(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================
# 📄 GET DOCTOR BY ID
# ==================================
@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_by_id(doctor_id: str):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ==================================
# ✏ UPDATE DOCTOR
# ==================================
@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update(doctor_id: str, payload: DoctorUpdate):
    updated = update_doctor(doctor_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated


# ==================================
# 🟢 UPDATE DOCTOR STATUS
# ==================================
@router.patch("/{doctor_id}/status", response_model=DoctorResponse)
async def update_status(doctor_id: str, status_value: DoctorStatus):
    updated = update_doctor_status(doctor_id, status_value)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated


# ==================================
# 🗑 DELETE DOCTOR
# ==================================
@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(doctor_id: str):
    deleted = delete_doctor(doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return None


# ==================================
# 🕒 ADD DOCTOR AVAILABILITY
# ==================================
@router.post("/{doctor_id}/availability", status_code=status.HTTP_201_CREATED)
async def add_availability(doctor_id: str, payload: DoctorAvailability):
    return add_doctor_availability(doctor_id, payload)


# ==================================
# 📅 GET DOCTOR AVAILABILITY
# ==================================
@router.get("/{doctor_id}/availability", response_model=List[DoctorAvailability])
async def get_availability(doctor_id: str):
    return get_doctor_availability(doctor_id)


# ==================================
# 📊 DOCTOR STATISTICS
# ==================================
@router.get("/{doctor_id}/stats", response_model=DoctorStats)
async def doctor_stats(doctor_id: str):
    return get_doctor_statistics(doctor_id)