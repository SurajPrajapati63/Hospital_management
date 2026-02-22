from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, time
from enum import Enum

class DoctorStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_leave = "on_leave"


class ConsultationMode(str, Enum):
    in_person = "in_person"
    telemedicine = "telemedicine"
    both = "both"

class DoctorBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str]
    specialization: str = Field(..., max_length=100)
    department: Optional[str]
    experience_years: Optional[int] = Field(None, ge=0, le=60)
    consultation_fee: Optional[float] = Field(None, ge=0)
    consultation_mode: ConsultationMode = ConsultationMode.in_person




class DoctorCreate(DoctorBase):
    license_number: str = Field(..., max_length=50)




class DoctorUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    specialization: Optional[str]
    department: Optional[str]
    experience_years: Optional[int]
    consultation_fee: Optional[float]
    consultation_mode: Optional[ConsultationMode]
    status: Optional[DoctorStatus]

class DoctorAvailability(BaseModel):
    day_of_week: str  # e.g., Monday
    start_time: time
    end_time: time




class DoctorResponse(DoctorBase):
    id: int
    license_number: str
    status: DoctorStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True




class DoctorPublicView(BaseModel):
    id: int
    full_name: str
    specialization: str
    department: Optional[str]
    experience_years: Optional[int]
    consultation_fee: Optional[float]
    consultation_mode: ConsultationMode

    class Config:
        orm_mode = True



class DoctorFilter(BaseModel):
    specialization: Optional[str]
    department: Optional[str]
    consultation_mode: Optional[ConsultationMode]
    status: Optional[DoctorStatus]
    min_experience: Optional[int]
    max_fee: Optional[float]

class DoctorStats(BaseModel):
    doctor_id: int
    total_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    average_rating: Optional[float]




class DoctorAIContext(BaseModel):
    doctor_id: int
    specialization: str
    recent_cases_summary: Optional[str]
    average_consultation_time: Optional[int]



from pydantic import validator

class DoctorAvailability(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time

    @validator("end_time")
    def validate_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("End time must be after start time")
        return v