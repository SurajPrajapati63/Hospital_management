from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ==========================================
# 💊 DOSAGE FORM ENUM
# ==========================================

class DosageForm(str, Enum):
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"
    injection = "injection"
    ointment = "ointment"
    drops = "drops"
    inhaler = "inhaler"
    other = "other"

class PrescriptionMedicine(BaseModel):
    medicine_name: str = Field(..., min_length=2, max_length=100)
    strength: str = Field(..., description="Example: 500mg")
    dosage_form: DosageForm
    duration_days: int = Field(..., ge=1, le=365)
    quantity: int = Field(..., ge=1)
    instructions: Optional[str] = None

   
# ==========================================
# 🕒 FREQUENCY ENUM
# ==========================================

class Frequency(str, Enum):
    once_daily = "once_daily"
    twice_daily = "twice_daily"
    thrice_daily = "thrice_daily"
    four_times_daily = "four_times_daily"
    weekly = "weekly"
    as_needed = "as_needed"


# ==========================================
# 💊 MEDICATION ITEM
# ==========================================

class MedicationItem(BaseModel):
    medicine_name: str = Field(..., min_length=2, max_length=100)
    dosage: str = Field(..., description="Example: 500mg")
    dosage_form: DosageForm
    frequency: Frequency
    duration_days: int = Field(..., ge=1)
    instructions: Optional[str] = None


# ==========================================
# 📝 BASE PRESCRIPTION MODEL
# ==========================================

class PrescriptionBase(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    diagnosis: Optional[str] = None
    medications: List[MedicationItem]
    notes: Optional[str] = None


# ==========================================
# ➕ CREATE PRESCRIPTION
# ==========================================

class PrescriptionCreate(PrescriptionBase):
    pass


# ==========================================
# ✏ UPDATE PRESCRIPTION
# ==========================================

class PrescriptionUpdate(BaseModel):
    diagnosis: Optional[str]
    medications: Optional[List[MedicationItem]]
    notes: Optional[str]


# ==========================================
# 📤 PRESCRIPTION RESPONSE
# ==========================================

class PrescriptionResponse(PrescriptionBase):
    id: str
    issued_date: date
    valid_until: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# ==========================================
# 🔍 FILTER PRESCRIPTION
# ==========================================

class PrescriptionFilter(BaseModel):
    patient_id: Optional[str]
    doctor_id: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


# ==========================================
# 📊 PRESCRIPTION STATS
# ==========================================

class PrescriptionStats(BaseModel):
    total_prescriptions: int
    active_prescriptions: int
    expired_prescriptions: int


# ==========================================
# 🤖 AI CONTEXT FOR EXPLANATION
# ==========================================

class PrescriptionAIContext(BaseModel):
    prescription_id: str
    patient_age: Optional[int]
    chronic_conditions: Optional[List[str]]
    allergies: Optional[List[str]]