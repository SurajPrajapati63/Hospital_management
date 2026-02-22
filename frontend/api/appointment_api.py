from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.models.appointment_model import (
    Appointment,
    create_appointment,
    get_all_appointments,
    get_appointment_by_id,
    update_appointment,
    delete_appointment
)

router = APIRouter()

# ----------------------------
# Create Appointment
# ----------------------------
@router.post("/appointments", response_model=dict)
async def add_appointment(appointment: Appointment):
    appointment_id = await create_appointment(appointment)
    return {"id": appointment_id, "message": "Appointment created successfully"}


# ----------------------------
# Get All Appointments
# ----------------------------
@router.get("/appointments", response_model=List[dict])
async def list_appointments():
    return await get_all_appointments()


# ----------------------------
# Get Appointment by ID
# ----------------------------
@router.get("/appointments/{appointment_id}", response_model=dict)
async def get_appointment(appointment_id: str):
    appointment = await get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# ----------------------------
# Update Appointment
# ----------------------------
@router.put("/appointments/{appointment_id}", response_model=dict)
async def update_appointment_api(appointment_id: str, update_data: dict):
    updated_count = await update_appointment(appointment_id, update_data)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found or no changes made")
    return {"message": "Appointment updated successfully"}


# ----------------------------
# Delete Appointment
# ----------------------------
@router.delete("/appointments/{appointment_id}", response_model=dict)
async def delete_appointment_api(appointment_id: str):
    deleted_count = await delete_appointment(appointment_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}