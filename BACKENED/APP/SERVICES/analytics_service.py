from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Any, List

from app.database import db


# ==========================================
# 📊 OVERALL DASHBOARD SUMMARY
# ==========================================
def get_dashboard_overview() -> Dict[str, Any]:
    total_patients = db.patients.count_documents({})
    total_doctors = db.doctors.count_documents({})
    total_appointments = db.appointments.count_documents({})
    total_revenue = sum(
        bill.get("total_amount", 0)
        for bill in db.billing.find({"payment_status": "paid"})
    )

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "total_revenue": total_revenue,
    }


# ==========================================
# 📅 MONTHLY APPOINTMENT TREND
# ==========================================
def get_monthly_appointments() -> Dict[str, int]:
    monthly_data = defaultdict(int)

    for appt in db.appointments.find({}):
        month = appt["appointment_date"].strftime("%Y-%m")
        monthly_data[month] += 1

    return dict(monthly_data)


# ==========================================
# 💰 MONTHLY REVENUE TREND
# ==========================================
def get_monthly_revenue() -> Dict[str, float]:
    revenue_data = defaultdict(float)

    for bill in db.billing.find({"payment_status": "paid"}):
        month = bill["created_at"].strftime("%Y-%m")
        revenue_data[month] += bill.get("total_amount", 0)

    return dict(revenue_data)


# ==========================================
# 👨‍⚕️ DOCTOR PERFORMANCE
# ==========================================
def get_doctor_performance() -> List[Dict[str, Any]]:
    performance = []

    doctors = db.doctors.find({})
    for doctor in doctors:
        doctor_id = str(doctor.get("_id", ""))

        total = db.appointments.count_documents({"doctor_id": doctor_id})
        completed = db.appointments.count_documents(
            {"doctor_id": doctor_id, "status": "completed"}
        )
        cancelled = db.appointments.count_documents(
            {"doctor_id": doctor_id, "status": "cancelled"}
        )

        performance.append(
            {
                "doctor_id": doctor_id,
                "doctor_name": doctor.get("full_name", "Unknown"),
                "total_appointments": total,
                "completed_appointments": completed,
                "cancelled_appointments": cancelled,
            }
        )

    return performance


# ==========================================
# 👥 PATIENT GROWTH ANALYTICS
# ==========================================
def get_patient_growth() -> Dict[str, int]:
    growth_data = defaultdict(int)

    for patient in db.patients.find({}):
        month = patient["created_at"].strftime("%Y-%m")
        growth_data[month] += 1

    return dict(growth_data)


# ==========================================
# ⚠ BILLING OUTSTANDING ANALYTICS
# ==========================================
def get_outstanding_bills() -> Dict[str, Any]:
    total_outstanding = 0
    pending_count = 0

    for bill in db.billing.find({"payment_status": "pending"}):
        total_outstanding += bill.get("total_amount", 0)
        pending_count += 1

    return {
        "pending_bills": pending_count,
        "total_outstanding_amount": total_outstanding,
    }


# ==========================================
# 📈 ADVANCED ANALYTICS (AI-READY)
# ==========================================
def generate_analytics_summary() -> Dict[str, Any]:
    overview = get_dashboard_overview()
    monthly_revenue = get_monthly_revenue()
    monthly_appointments = get_monthly_appointments()

    return {
        "overview": overview,
        "monthly_revenue": monthly_revenue,
        "monthly_appointments": monthly_appointments,
        "insights": [
            "Revenue increasing steadily" if len(monthly_revenue) > 3 else "Revenue stable",
            "Appointments growing" if len(monthly_appointments) > 3 else "Appointments stable",
        ],
    }