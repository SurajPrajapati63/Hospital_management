from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==========================================
# 💳 PAYMENT STATUS ENUM
# ==========================================

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    partially_paid = "partially_paid"
    cancelled = "cancelled"


# ==========================================
# 🏷 SERVICE ITEM (Line Item in Bill)
# ==========================================

class ServiceItem(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)
    amount: float = Field(..., ge=0)


# ==========================================
# 🧾 BASE BILL MODEL
# ==========================================

class BillingBase(BaseModel):
    patient_id: str
    appointment_id: Optional[str] = None
    services: List[ServiceItem]
    notes: Optional[str] = None


# ==========================================
# ➕ CREATE BILL
# ==========================================

class BillingCreate(BillingBase):
    pass


# ==========================================
# ✏ UPDATE BILL
# ==========================================

class BillingUpdate(BaseModel):
    services: Optional[List[ServiceItem]] = None
    notes: Optional[str] = None
    payment_status: Optional[PaymentStatus] = None


# ==========================================
# 📤 BILL RESPONSE
# ==========================================

class BillingResponse(BillingBase):
    id: str
    total_amount: float
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# ==========================================
# 📊 BILL FILTER
# ==========================================
class BillingStatsResponse(BaseModel):
    total_bills: int
    paid_bills: int
    pending_bills: int
    refunded_bills: int
    partially_paid_bills: int
    cancelled_bills: int

    total_revenue: float
    total_pending_amount: float
    total_refunded_amount: float
class BillingFilter(BaseModel):
    patient_id: Optional[str]
    payment_status: Optional[PaymentStatus]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


# ==========================================
# 📈 BILL STATS (For Analytics)
# ==========================================

class BillingStats(BaseModel):
    total_bills: int
    paid_bills: int
    pending_bills: int
    refunded_bills: int
    total_revenue: float


# ==========================================
# 🤖 BILL AI CONTEXT
# ==========================================

class BillingAIContext(BaseModel):
    patient_id: str
    total_amount: float
    services_summary: Optional[str]
    payment_status: PaymentStatus