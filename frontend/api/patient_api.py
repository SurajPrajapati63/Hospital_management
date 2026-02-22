"""
Patient API Client Module
Handles all frontend HTTP requests to patient backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
PATIENT_ENDPOINT = f"{BASE_URL}/patients"


class PatientAPIClient:
    """HTTP client for patient-related operations"""

    @staticmethod
    def create_patient(patient_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new patient"""
        try:
            response = requests.post(
                PATIENT_ENDPOINT,
                json=patient_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating patient: {str(e)}")
            return None

    @staticmethod
    def get_all_patients() -> Optional[List[Dict[str, Any]]]:
        """Fetch all patients"""
        try:
            response = requests.get(PATIENT_ENDPOINT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patients: {str(e)}")
            return None

    @staticmethod
    def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific patient by ID"""
        try:
            response = requests.get(f"{PATIENT_ENDPOINT}/{patient_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient: {str(e)}")
            return None

    @staticmethod
    def update_patient(patient_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update patient information"""
        try:
            response = requests.put(
                f"{PATIENT_ENDPOINT}/{patient_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating patient: {str(e)}")
            return None

    @staticmethod
    def delete_patient(patient_id: str) -> bool:
        """Delete a patient"""
        try:
            response = requests.delete(f"{PATIENT_ENDPOINT}/{patient_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting patient: {str(e)}")
            return False

    @staticmethod
    def get_patient_stats() -> Optional[Dict[str, Any]]:
        """Get patient statistics"""
        try:
            response = requests.get(f"{PATIENT_ENDPOINT}/stats/overview")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient stats: {str(e)}")
            return None

    @staticmethod
    def update_medical_history(patient_id: str, condition: str, description: str) -> Optional[Dict[str, Any]]:
        """Add medical history to patient"""
        try:
            response = requests.patch(
                f"{PATIENT_ENDPOINT}/{patient_id}/medical-history",
                json={"condition": condition, "description": description},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating medical history: {str(e)}")
            return None

    @staticmethod
    def get_patient_ai_context(patient_id: str) -> Optional[Dict[str, Any]]:
        """Get AI context for patient (medical history, ongoing conditions)"""
        try:
            response = requests.get(f"{PATIENT_ENDPOINT}/{patient_id}/ai-context")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient AI context: {str(e)}")
            return None


# Convenience functions for direct use
def create_patient(patient_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new patient"""
    return PatientAPIClient.create_patient(patient_data)


def get_all_patients() -> Optional[List[Dict[str, Any]]]:
    """Fetch all patients"""
    return PatientAPIClient.get_all_patients()


def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific patient by ID"""
    return PatientAPIClient.get_patient_by_id(patient_id)


def update_patient(patient_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update patient information"""
    return PatientAPIClient.update_patient(patient_id, update_data)


def delete_patient(patient_id: str) -> bool:
    """Delete a patient"""
    return PatientAPIClient.delete_patient(patient_id)


def get_patient_stats() -> Optional[Dict[str, Any]]:
    """Get patient statistics"""
    return PatientAPIClient.get_patient_stats()


def update_medical_history(patient_id: str, condition: str, description: str) -> Optional[Dict[str, Any]]:
    """Add medical history to patient"""
    return PatientAPIClient.update_medical_history(patient_id, condition, description)


def get_patient_ai_context(patient_id: str) -> Optional[Dict[str, Any]]:
    """Get AI context for patient"""
    return PatientAPIClient.get_patient_ai_context(patient_id)