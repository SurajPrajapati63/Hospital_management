
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ----------------------------
# Patient Form
# ----------------------------
class PatientForm(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None


# ----------------------------
# Doctor Form
# ----------------------------
class DoctorForm(BaseModel):
    name: str
    specialization: str
    experience: int
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None


# ----------------------------
# Appointment Form
# ----------------------------
class AppointmentForm(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: str  # YYYY-MM-DD
    appointment_time: str  # HH:MM
    reason: Optional[str] = None
    status: Optional[str] = "Scheduled"


# ----------------------------
# Billing Form
# ----------------------------
class BillingForm(BaseModel):
    patient_id: str
    appointment_id: Optional[str] = None
    doctor_id: str
    services: List[str]
    total_amount: float
    status: Optional[str] = "Unpaid"  # Paid / Unpaid
    payment_method: Optional[str] = None
    billing_date: Optional[str] = None  # YYYY-MM-DD


# ----------------------------
# Prescription Form
# ----------------------------
class PrescriptionForm(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    medicines: List[str]
    dosage: List[str]
    instructions: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    notes: Optional[str] = None


# ----------------------------
# Report Form
# ----------------------------
class ReportForm(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    report_type: str  # e.g., Blood Test, X-ray, MRI
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    file_url: Optional[str] = None


# ----------------------------
# User Form (for auth)
# ----------------------------
class UserForm(BaseModel):
    username: str
    password: str
    role: str  # admin / doctor / patient