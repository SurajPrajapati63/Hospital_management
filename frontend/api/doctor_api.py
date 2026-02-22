"""
Doctor API Client Module
Handles all frontend HTTP requests to doctor backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
DOCTOR_ENDPOINT = f"{BASE_URL}/doctors"


class DoctorAPIClient:
    """HTTP client for doctor-related operations"""

    @staticmethod
    def create_doctor(doctor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new doctor"""
        try:
            response = requests.post(
                DOCTOR_ENDPOINT,
                json=doctor_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating doctor: {str(e)}")
            return None

    @staticmethod
    def get_all_doctors() -> Optional[List[Dict[str, Any]]]:
        """Fetch all doctors"""
        try:
            response = requests.get(DOCTOR_ENDPOINT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctors: {str(e)}")
            return None

    @staticmethod
    def get_doctor_by_id(doctor_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific doctor by ID"""
        try:
            response = requests.get(f"{DOCTOR_ENDPOINT}/{doctor_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor: {str(e)}")
            return None

    @staticmethod
    def update_doctor(doctor_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update doctor information"""
        try:
            response = requests.put(
                f"{DOCTOR_ENDPOINT}/{doctor_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating doctor: {str(e)}")
            return None

    @staticmethod
    def delete_doctor(doctor_id: str) -> bool:
        """Delete a doctor"""
        try:
            response = requests.delete(f"{DOCTOR_ENDPOINT}/{doctor_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting doctor: {str(e)}")
            return False

    @staticmethod
    def update_doctor_status(doctor_id: str, status: str) -> Optional[Dict[str, Any]]:
        """Update doctor availability status"""
        try:
            response = requests.patch(
                f"{DOCTOR_ENDPOINT}/{doctor_id}/status",
                json={"status": status},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating doctor status: {str(e)}")
            return None

    @staticmethod
    def add_doctor_availability(doctor_id: str, day: str, start_time: str, end_time: str) -> Optional[Dict[str, Any]]:
        """Add availability slot for doctor"""
        try:
            response = requests.post(
                f"{DOCTOR_ENDPOINT}/{doctor_id}/availability",
                json={"day": day, "start_time": start_time, "end_time": end_time},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error adding doctor availability: {str(e)}")
            return None

    @staticmethod
    def get_doctor_availability(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get doctor availability schedule"""
        try:
            response = requests.get(f"{DOCTOR_ENDPOINT}/{doctor_id}/availability")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor availability: {str(e)}")
            return None

    @staticmethod
    def get_doctor_statistics(doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get doctor statistics and performance metrics"""
        try:
            response = requests.get(f"{DOCTOR_ENDPOINT}/{doctor_id}/stats")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor statistics: {str(e)}")
            return None


# Convenience functions for direct use
def create_doctor(doctor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new doctor"""
    return DoctorAPIClient.create_doctor(doctor_data)


def get_all_doctors() -> Optional[List[Dict[str, Any]]]:
    """Fetch all doctors"""
    return DoctorAPIClient.get_all_doctors()


def get_doctor_by_id(doctor_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific doctor by ID"""
    return DoctorAPIClient.get_doctor_by_id(doctor_id)


def update_doctor(doctor_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update doctor information"""
    return DoctorAPIClient.update_doctor(doctor_id, update_data)


def delete_doctor(doctor_id: str) -> bool:
    """Delete a doctor"""
    return DoctorAPIClient.delete_doctor(doctor_id)


def update_doctor_status(doctor_id: str, status: str) -> Optional[Dict[str, Any]]:
    """Update doctor availability status"""
    return DoctorAPIClient.update_doctor_status(doctor_id, status)


def add_doctor_availability(doctor_id: str, day: str, start_time: str, end_time: str) -> Optional[Dict[str, Any]]:
    """Add availability slot for doctor"""
    return DoctorAPIClient.add_doctor_availability(doctor_id, day, start_time, end_time)


def get_doctor_availability(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get doctor availability schedule"""
    return DoctorAPIClient.get_doctor_availability(doctor_id)


def get_doctor_statistics(doctor_id: str) -> Optional[Dict[str, Any]]:
    """Get doctor statistics and performance metrics"""
    return DoctorAPIClient.get_doctor_statistics(doctor_id)
