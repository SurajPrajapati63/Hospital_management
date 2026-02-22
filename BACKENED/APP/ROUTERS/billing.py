from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from app.schemas.billing_schema import (
    BillingCreate,
    BillingUpdate,
    BillingResponse,
    BillingStatsResponse
)

from app.services.billing_service import (
    create_bill,
    get_bill_by_id,
    get_all_bills,
    update_bill,
    delete_bill,
    mark_bill_paid,
    refund_bill,
    get_patient_bills,
    get_billing_statistics,
)

router = APIRouter(prefix="/billing", tags=["Billing"])


# ==================================
# 💰 CREATE BILL
# ==================================
@router.post("/", response_model=BillingResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: BillingCreate):
    try:
        return create_bill(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================================
# 📄 GET BILL BY ID
# ==================================
@router.get("/{bill_id}", response_model=BillingResponse)
async def get_by_id(bill_id: str):
    bill = get_bill_by_id(bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


# ==================================
# 📋 GET ALL BILLS (WITH FILTER)
# ==================================
@router.get("/", response_model=List[BillingResponse])
async def get_all(
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    try:
        return get_all_bills(
            patient_id=patient_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================================
# 👤 GET PATIENT BILLS
# ==================================
@router.get("/patient/{patient_id}", response_model=List[BillingResponse])
async def patient_bills(patient_id: str):
    return get_patient_bills(patient_id)


# ==================================
# ✏ UPDATE BILL
# ==================================
@router.put("/{bill_id}", response_model=BillingResponse)
async def update(bill_id: str, payload: BillingUpdate):
    updated = update_bill(bill_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Bill not found")
    return updated


# ==================================
# ✅ MARK BILL AS PAID
# ==================================
@router.patch("/{bill_id}/pay", response_model=BillingResponse)
async def pay_bill(bill_id: str):
    paid = mark_bill_paid(bill_id)
    if not paid:
        raise HTTPException(status_code=404, detail="Bill not found")
    return paid


# ==================================
# 🔁 REFUND BILL
# ==================================
@router.patch("/{bill_id}/refund", response_model=BillingResponse)
async def refund(bill_id: str):
    refunded = refund_bill(bill_id)
    if not refunded:
        raise HTTPException(status_code=404, detail="Bill not found")
    return refunded


# ==================================
# 🗑 DELETE BILL
# ==================================
@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(bill_id: str):
    deleted = delete_bill(bill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bill not found")
    return None


# ==================================
# 📊 BILLING STATISTICS
# ==================================
@router.get("/stats/overview", response_model=BillingStatsResponse)
async def billing_stats():
    return get_billing_statistics()