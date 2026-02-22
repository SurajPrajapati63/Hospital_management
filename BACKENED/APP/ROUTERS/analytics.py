"""
Analytics Router
Handles all analytics and reporting endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List, Optional

from app.services.analytics_service import (
    get_dashboard_overview,
    get_monthly_appointments,
    get_monthly_revenue,
    get_doctor_performance,
    get_patient_growth,
    get_outstanding_bills,
    generate_analytics_summary,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ==================================
# 📊 DASHBOARD OVERVIEW
# ==================================
@router.get("/dashboard", response_model=Dict[str, Any])
async def dashboard_overview():
    """Get dashboard overview with key metrics"""
    data = get_dashboard_overview()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard data")
    return data


# ==================================
# 📈 MONTHLY APPOINTMENTS
# ==================================
@router.get("/appointments/monthly", response_model=Dict[str, Any])
async def monthly_appointments():
    """Get monthly appointment statistics"""
    data = get_monthly_appointments()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch appointment data")
    return data


# ==================================
# 💰 MONTHLY REVENUE
# ==================================
@router.get("/revenue/monthly", response_model=Dict[str, Any])
async def monthly_revenue():
    """Get monthly revenue statistics"""
    data = get_monthly_revenue()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch revenue data")
    return data


# ==================================
# 👨‍⚕️ DOCTOR PERFORMANCE
# ==================================
@router.get("/doctors/performance", response_model=List[Dict[str, Any]])
async def doctor_performance():
    """Get doctor performance metrics"""
    data = get_doctor_performance()
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Failed to fetch doctor performance data")
    return data


# ==================================
# 📊 PATIENT GROWTH
# ==================================
@router.get("/patients/growth", response_model=Dict[str, Any])
async def patient_growth():
    """Get patient growth trends"""
    data = get_patient_growth()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch patient growth data")
    return data


# ==================================
# 💳 OUTSTANDING BILLS
# ==================================
@router.get("/bills/outstanding", response_model=Dict[str, Any])
async def outstanding_bills():
    """Get outstanding bills summary"""
    data = get_outstanding_bills()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch outstanding bills")
    return data


# ==================================
# 📋 COMPREHENSIVE SUMMARY
# ==================================
@router.get("/summary", response_model=Dict[str, Any])
async def analytics_summary():
    """Generate comprehensive analytics summary"""
    data = generate_analytics_summary()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to generate analytics summary")
    return data
