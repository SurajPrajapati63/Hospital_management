from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.prescription_schema import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionMedicine,
)

from app.schemas.ai_schema import (
    PrescriptionExplanationRequest,
    PrescriptionExplanationResponse,
)

from app.services.prescription_service import (
    create_prescription,
    get_prescription_by_id,
    get_patient_prescriptions,
    get_doctor_prescriptions,
    update_prescription,
    delete_prescription,
    add_medicine_to_prescription,
   
)



router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


# ==================================
# 📝 CREATE PRESCRIPTION
# ==================================
@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: PrescriptionCreate):
    try:
        return create_prescription(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 📄 GET PRESCRIPTION BY ID
# ==================================
@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_by_id(prescription_id: str):
    prescription = get_prescription_by_id(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription


# ==================================
# 👤 GET PATIENT PRESCRIPTIONS
# ==================================
@router.get("/patient/{patient_id}", response_model=List[PrescriptionResponse])
async def patient_prescriptions(patient_id: str):
    return get_patient_prescriptions(patient_id)


# ==================================
# 👨‍⚕️ GET DOCTOR PRESCRIPTIONS
# ==================================
@router.get("/doctor/{doctor_id}", response_model=List[PrescriptionResponse])
async def doctor_prescriptions(doctor_id: str):
    return get_doctor_prescriptions(doctor_id)


# ==================================
# ✏ UPDATE PRESCRIPTION
# ==================================
@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update(prescription_id: str, payload: PrescriptionUpdate):
    updated = update_prescription(prescription_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return updated


# ==================================
# ➕ ADD MEDICINE TO PRESCRIPTION
# ==================================
@router.post("/{prescription_id}/add-medicine", response_model=PrescriptionResponse)
async def add_medicine(prescription_id: str, payload: PrescriptionMedicine):
    updated = add_medicine_to_prescription(prescription_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return updated


# ==================================
# 🗑 DELETE PRESCRIPTION
# ==================================
@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(prescription_id: str):
    deleted = delete_prescription(prescription_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return None


# ==================================
# 🤖 AI EXPLAIN PRESCRIPTION
# ==================================
@router.post("/{prescription_id}/explain", response_model=PrescriptionExplanationResponse)
async def explain(prescription_id: str):
    prescription = get_prescription_by_id(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    # Create explanation response from prescription data
    medicines_text = ", ".join([m.get("name", "Unknown") for m in prescription.get("medicines", [])])
    
    explanation = PrescriptionExplanationResponse(
        explanation=f"This prescription contains the following medicines: {medicines_text}. " +
                   f"Take as prescribed by your doctor. If you experience any adverse effects, please contact your healthcare provider.",
        warnings=["Take with food if stomach upset occurs", "Consult doctor before taking other medications"],
        side_effects=["Mild side effects may occur", "Contact doctor if symptoms persist"]
    )

    return explanation