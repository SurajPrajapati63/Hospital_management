from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"
    rescheduled = "rescheduled"


class AppointmentType(str, Enum):
    consultation = "consultation"
    follow_up = "follow_up"
    emergency = "emergency"
    telemedicine = "telemedicine"


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    appointment_type: AppointmentType
    reason: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime]
    appointment_type: Optional[AppointmentType]
    status: Optional[AppointmentStatus]
    reason: Optional[str]
    notes: Optional[str]


class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class AppointmentDetail(BaseModel):
    id: int
    appointment_date: datetime
    appointment_type: AppointmentType
    status: AppointmentStatus
    reason: Optional[str]
    notes: Optional[str]

    patient_name: str
    doctor_name: str
    department: Optional[str]

    class Config:
        orm_mode = True


class AppointmentFilter(BaseModel):
    doctor_id: Optional[int]
    patient_id: Optional[int]
    status: Optional[AppointmentStatus]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class AppointmentAIContext(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    symptoms: Optional[str]
    previous_history: Optional[str]


class AppointmentPatientView(BaseModel):
    id: int
    appointment_date: datetime
    appointment_type: AppointmentType
    status: AppointmentStatus
    doctor_name: str

    class Config:
        orm_mode = True