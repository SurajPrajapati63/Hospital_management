"""
Prescription API Client Module
Handles all frontend HTTP requests to prescription backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
PRESCRIPTION_ENDPOINT = f"{BASE_URL}/prescriptions"


class PrescriptionAPIClient:
    """HTTP client for prescription-related operations"""

    @staticmethod
    def create_prescription(prescription_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new prescription"""
        try:
            response = requests.post(
                PRESCRIPTION_ENDPOINT,
                json=prescription_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating prescription: {str(e)}")
            return None

    @staticmethod
    def get_all_prescriptions() -> Optional[List[Dict[str, Any]]]:
        """Fetch all prescriptions"""
        try:
            response = requests.get(PRESCRIPTION_ENDPOINT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prescriptions: {str(e)}")
            return None

    @staticmethod
    def get_prescription_by_id(prescription_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific prescription by ID"""
        try:
            response = requests.get(f"{PRESCRIPTION_ENDPOINT}/{prescription_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prescription: {str(e)}")
            return None

    @staticmethod
    def update_prescription(prescription_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update prescription information"""
        try:
            response = requests.put(
                f"{PRESCRIPTION_ENDPOINT}/{prescription_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating prescription: {str(e)}")
            return None

    @staticmethod
    def delete_prescription(prescription_id: str) -> bool:
        """Delete a prescription"""
        try:
            response = requests.delete(f"{PRESCRIPTION_ENDPOINT}/{prescription_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting prescription: {str(e)}")
            return False

    @staticmethod
    def get_patient_prescriptions(patient_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get all prescriptions for a patient"""
        try:
            response = requests.get(f"{PRESCRIPTION_ENDPOINT}/patient/{patient_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient prescriptions: {str(e)}")
            return None

    @staticmethod
    def get_doctor_prescriptions(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get all prescriptions issued by a doctor"""
        try:
            response = requests.get(f"{PRESCRIPTION_ENDPOINT}/doctor/{doctor_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor prescriptions: {str(e)}")
            return None

    @staticmethod
    def add_medicine_to_prescription(prescription_id: str, medicine_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add a medicine to an existing prescription"""
        try:
            response = requests.post(
                f"{PRESCRIPTION_ENDPOINT}/{prescription_id}/medicines",
                json=medicine_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error adding medicine to prescription: {str(e)}")
            return None


# Convenience functions for direct use
def create_prescription(prescription_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new prescription"""
    return PrescriptionAPIClient.create_prescription(prescription_data)


def get_all_prescriptions() -> Optional[List[Dict[str, Any]]]:
    """Fetch all prescriptions"""
    return PrescriptionAPIClient.get_all_prescriptions()


def get_prescription_by_id(prescription_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific prescription by ID"""
    return PrescriptionAPIClient.get_prescription_by_id(prescription_id)


def update_prescription(prescription_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update prescription information"""
    return PrescriptionAPIClient.update_prescription(prescription_id, update_data)


def delete_prescription(prescription_id: str) -> bool:
    """Delete a prescription"""
    return PrescriptionAPIClient.delete_prescription(prescription_id)


def get_patient_prescriptions(patient_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get all prescriptions for a patient"""
    return PrescriptionAPIClient.get_patient_prescriptions(patient_id)


def get_doctor_prescriptions(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get all prescriptions issued by a doctor"""
    return PrescriptionAPIClient.get_doctor_prescriptions(doctor_id)


def add_medicine_to_prescription(prescription_id: str, medicine_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Add a medicine to an existing prescription"""
    return PrescriptionAPIClient.add_medicine_to_prescription(prescription_id, medicine_data)
