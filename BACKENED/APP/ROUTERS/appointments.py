from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentDetail,
    AppointmentFilter,
    AppointmentPatientView,
)

from app.services.appointment_service import (
    create_appointment,
    get_appointment_by_id,
    get_all_appointments,
    update_appointment,
    delete_appointment,
    cancel_appointment,
    get_patient_appointments,
    get_doctor_appointments,
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# ==================================
# 📌 CREATE APPOINTMENT
# ==================================
@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: AppointmentCreate):
    try:
        return create_appointment(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 📌 GET ALL APPOINTMENTS (WITH FILTER)
# ==================================
@router.get("/", response_model=List[AppointmentResponse])
async def get_all(
    doctor_id: Optional[str] = None,
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    try:
        filters = AppointmentFilter(
            doctor_id=doctor_id,
            patient_id=patient_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        return get_all_appointments(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================
# 📌 GET APPOINTMENT BY ID
# ==================================
@router.get("/{appointment_id}", response_model=AppointmentDetail)
async def get_by_id(appointment_id: str):
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# ==================================
# 📌 UPDATE APPOINTMENT
# ==================================
@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update(appointment_id: str, payload: AppointmentUpdate):
    updated = update_appointment(appointment_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated


# ==================================
# ❌ CANCEL APPOINTMENT
# ==================================
@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel(appointment_id: str):
    cancelled = cancel_appointment(appointment_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return cancelled


# ==================================
# 🗑 DELETE APPOINTMENT
# ==================================
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(appointment_id: str):
    deleted = delete_appointment(appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return None


# ==================================
# 👤 PATIENT VIEW
# ==================================
@router.get("/patient/{patient_id}", response_model=List[AppointmentPatientView])
async def patient_view(patient_id: str):
    return get_patient_appointments(patient_id)


# ==================================
# 👨‍⚕️ DOCTOR VIEW
# ==================================
@router.get("/doctor/{doctor_id}", response_model=List[AppointmentResponse])
async def doctor_view(doctor_id: str):
    return get_doctor_appointments(doctor_id)