"""
Billing API Client Module
Handles all frontend HTTP requests to billing backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
BILLING_ENDPOINT = f"{BASE_URL}/billing"


class BillingAPIClient:
    """HTTP client for billing-related operations"""

    @staticmethod
    def create_bill(bill_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new bill (auto-calculates totals)"""
        try:
            response = requests.post(
                BILLING_ENDPOINT,
                json=bill_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating bill: {str(e)}")
            return None

    @staticmethod
    def get_all_bills() -> Optional[List[Dict[str, Any]]]:
        """Fetch all bills"""
        try:
            response = requests.get(BILLING_ENDPOINT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching bills: {str(e)}")
            return None

    @staticmethod
    def get_bill_by_id(bill_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific bill by ID"""
        try:
            response = requests.get(f"{BILLING_ENDPOINT}/{bill_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching bill: {str(e)}")
            return None

    @staticmethod
    def update_bill(bill_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update bill information"""
        try:
            response = requests.put(
                f"{BILLING_ENDPOINT}/{bill_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating bill: {str(e)}")
            return None

    @staticmethod
    def mark_bill_paid(bill_id: str, payment_method: str = "unknown") -> Optional[Dict[str, Any]]:
        """Mark a bill as paid"""
        try:
            response = requests.patch(
                f"{BILLING_ENDPOINT}/{bill_id}/paid",
                json={"payment_method": payment_method},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error marking bill as paid: {str(e)}")
            return None

    @staticmethod
    def refund_bill(bill_id: str) -> Optional[Dict[str, Any]]:
        """Refund a paid bill"""
        try:
            response = requests.patch(
                f"{BILLING_ENDPOINT}/{bill_id}/refund",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error refunding bill: {str(e)}")
            return None

    @staticmethod
    def delete_bill(bill_id: str) -> bool:
        """Delete a bill"""
        try:
            response = requests.delete(f"{BILLING_ENDPOINT}/{bill_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting bill: {str(e)}")
            return False

    @staticmethod
    def get_patient_bills(patient_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get all bills for a patient"""
        try:
            response = requests.get(f"{BILLING_ENDPOINT}/patient/{patient_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient bills: {str(e)}")
            return None

    @staticmethod
    def get_billing_statistics() -> Optional[Dict[str, Any]]:
        """Get billing statistics and financial overview"""
        try:
            response = requests.get(f"{BILLING_ENDPOINT}/stats/overview")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching billing statistics: {str(e)}")
            return None


# Convenience functions for direct use
def create_bill(bill_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new bill"""
    return BillingAPIClient.create_bill(bill_data)


def get_all_bills() -> Optional[List[Dict[str, Any]]]:
    """Fetch all bills"""
    return BillingAPIClient.get_all_bills()


def get_bill_by_id(bill_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific bill by ID"""
    return BillingAPIClient.get_bill_by_id(bill_id)


def update_bill(bill_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update bill information"""
    return BillingAPIClient.update_bill(bill_id, update_data)


def mark_bill_paid(bill_id: str, payment_method: str = "unknown") -> Optional[Dict[str, Any]]:
    """Mark a bill as paid"""
    return BillingAPIClient.mark_bill_paid(bill_id, payment_method)


def refund_bill(bill_id: str) -> Optional[Dict[str, Any]]:
    """Refund a paid bill"""
    return BillingAPIClient.refund_bill(bill_id)


def delete_bill(bill_id: str) -> bool:
    """Delete a bill"""
    return BillingAPIClient.delete_bill(bill_id)


def get_patient_bills(patient_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get all bills for a patient"""
    return BillingAPIClient.get_patient_bills(patient_id)


def get_billing_statistics() -> Optional[Dict[str, Any]]:
    """Get billing statistics and financial overview"""
    return BillingAPIClient.get_billing_statistics()
