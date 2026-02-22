from typing import List, Dict

# ----------------------------
# Table structure for patients
# ----------------------------
PATIENT_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "name", "headerName": "Name"},
    {"field": "age", "headerName": "Age"},
    {"field": "gender", "headerName": "Gender"},
    {"field": "phone", "headerName": "Phone"},
    {"field": "email", "headerName": "Email"},
    {"field": "address", "headerName": "Address"},
    {"field": "medical_history", "headerName": "Medical History"}
]

# ----------------------------
# Table structure for doctors
# ----------------------------
DOCTOR_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "name", "headerName": "Name"},
    {"field": "specialization", "headerName": "Specialization"},
    {"field": "experience", "headerName": "Experience (Years)"},
    {"field": "phone", "headerName": "Phone"},
    {"field": "email", "headerName": "Email"},
    {"field": "address", "headerName": "Address"}
]

# ----------------------------
# Table structure for appointments
# ----------------------------
APPOINTMENT_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "patient_id", "headerName": "Patient ID"},
    {"field": "doctor_id", "headerName": "Doctor ID"},
    {"field": "appointment_date", "headerName": "Date"},
    {"field": "appointment_time", "headerName": "Time"},
    {"field": "reason", "headerName": "Reason"},
    {"field": "status", "headerName": "Status"}
]

# ----------------------------
# Table structure for prescriptions
# ----------------------------
PRESCRIPTION_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "patient_id", "headerName": "Patient ID"},
    {"field": "doctor_id", "headerName": "Doctor ID"},
    {"field": "appointment_id", "headerName": "Appointment ID"},
    {"field": "medicines", "headerName": "Medicines"},
    {"field": "dosage", "headerName": "Dosage"},
    {"field": "instructions", "headerName": "Instructions"},
    {"field": "date", "headerName": "Date"},
    {"field": "notes", "headerName": "Notes"}
]

# ----------------------------
# Table structure for billing
# ----------------------------
BILLING_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "patient_id", "headerName": "Patient ID"},
    {"field": "appointment_id", "headerName": "Appointment ID"},
    {"field": "doctor_id", "headerName": "Doctor ID"},
    {"field": "services", "headerName": "Services"},
    {"field": "total_amount", "headerName": "Total Amount"},
    {"field": "status", "headerName": "Status"},
    {"field": "payment_method", "headerName": "Payment Method"},
    {"field": "billing_date", "headerName": "Billing Date"}
]

# ----------------------------
# Table structure for reports
# ----------------------------
REPORT_TABLE_COLUMNS: List[Dict[str, str]] = [
    {"field": "id", "headerName": "ID"},
    {"field": "patient_id", "headerName": "Patient ID"},
    {"field": "doctor_id", "headerName": "Doctor ID"},
    {"field": "appointment_id", "headerName": "Appointment ID"},
    {"field": "report_type", "headerName": "Report Type"},
    {"field": "findings", "headerName": "Findings"},
    {"field": "recommendations", "headerName": "Recommendations"},
    {"field": "date", "headerName": "Date"},
    {"field": "file_url", "headerName": "File URL"}
]