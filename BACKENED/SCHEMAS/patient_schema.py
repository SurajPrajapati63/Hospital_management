from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict
from datetime import datetime, date
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class BloodGroup(str, Enum):
    A_pos = "A+"
    A_neg = "A-"
    B_pos = "B+"
    B_neg = "B-"
    AB_pos = "AB+"
    AB_neg = "AB-"
    O_pos = "O+"
    O_neg = "O-"


class MaritalStatus(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

class PatientBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr]
    phone: Optional[str]
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup]
    marital_status: Optional[MaritalStatus]
    address: Optional[str]

class PatientCreate(PatientBase):
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    insurance_provider: Optional[str]
    insurance_number: Optional[str]


class PatientUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[Gender]
    blood_group: Optional[BloodGroup]
    marital_status: Optional[MaritalStatus]
    address: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    insurance_provider: Optional[str]
    insurance_number: Optional[str]


class MedicalHistory(BaseModel):
    allergies: Optional[List[str]]
    chronic_diseases: Optional[List[str]]
    past_surgeries: Optional[List[str]]
    current_medications: Optional[List[str]]
    family_history: Optional[List[str]]

class PatientResponse(PatientBase):
    id: int
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    insurance_provider: Optional[str]
    insurance_number: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PatientPublicView(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup]
    allergies: Optional[List[str]]

    class Config:
        orm_mode = True


class PatientFilter(BaseModel):
    gender: Optional[Gender]
    blood_group: Optional[BloodGroup]
    min_age: Optional[int]
    max_age: Optional[int]
    chronic_disease: Optional[str]


class PatientStats(BaseModel):
    total_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    total_bills: Optional[float]
    outstanding_balance: Optional[float]


class PatientAIContext(BaseModel):
    patient_id: int
    age: int
    gender: Gender
    blood_group: Optional[BloodGroup]
    chronic_conditions: Optional[List[str]]
    allergies: Optional[List[str]]
    recent_reports_summary: Optional[str]

    patient_id: int
    accessed_by: int
    access_role: str
    timestamp: datetime
    action: str  # view / update / delete


@validator("date_of_birth")
def validate_age(cls, v):
    if v > date.today():
        raise ValueError("Date of birth cannot be in the future")
    return v
