from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

from app.database import db
from app.schemas.billing_schema import BillingCreate, BillingUpdate


# ==========================================
# 💰 CREATE BILL
# ==========================================
def create_bill(payload: BillingCreate):

    bill_data = payload.dict()

    # Auto-calculate total amount
    total_amount = sum(item["amount"] for item in bill_data.get("services", []))
    bill_data["total_amount"] = total_amount

    bill_data.update({
        "payment_status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": None
    })

    result = db.billing.insert_one(bill_data)
    bill_data["id"] = str(result.inserted_id)

    return bill_data


# ==========================================
# 📄 GET BILL BY ID
# ==========================================
def get_bill_by_id(bill_id: str):
    bill = db.billing.find_one({"_id": ObjectId(bill_id)})
    if bill:
        bill["id"] = str(bill["_id"])
    return bill


# ==========================================
# 📋 GET ALL BILLS (FILTERABLE)
# ==========================================
def get_all_bills(
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):

    query = {}

    if patient_id:
        query["patient_id"] = patient_id

    if status:
        query["payment_status"] = status

    if start_date and end_date:
        query["created_at"] = {
            "$gte": start_date,
            "$lte": end_date
        }

    bills = list(db.billing.find(query))

    for bill in bills:
        bill["id"] = str(bill["_id"])

    return bills


# ==========================================
# 👤 GET PATIENT BILLS
# ==========================================
def get_patient_bills(patient_id: str):

    bills = list(db.billing.find({"patient_id": patient_id}))

    for bill in bills:
        bill["id"] = str(bill["_id"])

    return bills


# ==========================================
# ✏ UPDATE BILL
# ==========================================
def update_bill(bill_id: str, payload: BillingUpdate):

    update_data = {k: v for k, v in payload.dict().items() if v is not None}

    # Recalculate total if services updated
    if "services" in update_data:
        update_data["total_amount"] = sum(
            item["amount"] for item in update_data["services"]
        )

    update_data["updated_at"] = datetime.utcnow()

    result = db.billing.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return None

    return get_bill_by_id(bill_id)


# ==========================================
# ✅ MARK BILL AS PAID
# ==========================================
def mark_bill_paid(bill_id: str):

    result = db.billing.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": {
            "payment_status": "paid",
            "paid_at": datetime.utcnow()
        }}
    )

    if result.modified_count == 0:
        return None

    return get_bill_by_id(bill_id)


# ==========================================
# 🔁 REFUND BILL
# ==========================================
def refund_bill(bill_id: str):

    result = db.billing.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": {
            "payment_status": "refunded",
            "refunded_at": datetime.utcnow()
        }}
    )

    if result.modified_count == 0:
        return None

    return get_bill_by_id(bill_id)


# ==========================================
# 🗑 DELETE BILL
# ==========================================
def delete_bill(bill_id: str):

    result = db.billing.delete_one({"_id": ObjectId(bill_id)})
    return result.deleted_count > 0


# ==========================================
# 📊 BILLING STATISTICS
# ==========================================
def get_billing_statistics() -> Dict[str, Any]:

    total_bills = db.billing.count_documents({})
    paid_bills = db.billing.count_documents({"payment_status": "paid"})
    pending_bills = db.billing.count_documents({"payment_status": "pending"})
    refunded_bills = db.billing.count_documents({"payment_status": "refunded"})

    total_revenue = sum(
        bill.get("total_amount", 0)
        for bill in db.billing.find({"payment_status": "paid"})
    )

    return {
        "total_bills": total_bills,
        "paid_bills": paid_bills,
        "pending_bills": pending_bills,
        "refunded_bills": refunded_bills,
        "total_revenue": total_revenue,
    }