"""
Appointment API Client Module
Handles all frontend HTTP requests to appointment backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
APPOINTMENT_ENDPOINT = f"{BASE_URL}/appointments"


class AppointmentAPIClient:
    """HTTP client for appointment-related operations"""

    @staticmethod
    def create_appointment(appointment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new appointment (with doctor availability checking)"""
        try:
            response = requests.post(
                APPOINTMENT_ENDPOINT,
                json=appointment_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating appointment: {str(e)}")
            return None

    @staticmethod
    def get_all_appointments() -> Optional[List[Dict[str, Any]]]:
        """Fetch all appointments"""
        try:
            response = requests.get(APPOINTMENT_ENDPOINT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching appointments: {str(e)}")
            return None

    @staticmethod
    def get_appointment_by_id(appointment_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific appointment by ID"""
        try:
            response = requests.get(f"{APPOINTMENT_ENDPOINT}/{appointment_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching appointment: {str(e)}")
            return None

    @staticmethod
    def update_appointment(appointment_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update appointment information"""
        try:
            response = requests.put(
                f"{APPOINTMENT_ENDPOINT}/{appointment_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating appointment: {str(e)}")
            return None

    @staticmethod
    def cancel_appointment(appointment_id: str) -> Optional[Dict[str, Any]]:
        """Cancel an appointment"""
        try:
            response = requests.patch(
                f"{APPOINTMENT_ENDPOINT}/{appointment_id}/cancel",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error canceling appointment: {str(e)}")
            return None

    @staticmethod
    def delete_appointment(appointment_id: str) -> bool:
        """Delete an appointment"""
        try:
            response = requests.delete(f"{APPOINTMENT_ENDPOINT}/{appointment_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting appointment: {str(e)}")
            return False

    @staticmethod
    def get_patient_appointments(patient_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get all appointments for a patient"""
        try:
            response = requests.get(f"{APPOINTMENT_ENDPOINT}/patient/{patient_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient appointments: {str(e)}")
            return None

    @staticmethod
    def get_doctor_appointments(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get all appointments for a doctor"""
        try:
            response = requests.get(f"{APPOINTMENT_ENDPOINT}/doctor/{doctor_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor appointments: {str(e)}")
            return None


# Convenience functions for direct use
def create_appointment(appointment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new appointment"""
    return AppointmentAPIClient.create_appointment(appointment_data)


def get_all_appointments() -> Optional[List[Dict[str, Any]]]:
    """Fetch all appointments"""
    return AppointmentAPIClient.get_all_appointments()


def get_appointment_by_id(appointment_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a specific appointment by ID"""
    return AppointmentAPIClient.get_appointment_by_id(appointment_id)


def update_appointment(appointment_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update appointment information"""
    return AppointmentAPIClient.update_appointment(appointment_id, update_data)


def cancel_appointment(appointment_id: str) -> Optional[Dict[str, Any]]:
    """Cancel an appointment"""
    return AppointmentAPIClient.cancel_appointment(appointment_id)


def delete_appointment(appointment_id: str) -> bool:
    """Delete an appointment"""
    return AppointmentAPIClient.delete_appointment(appointment_id)


def get_patient_appointments(patient_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get all appointments for a patient"""
    return AppointmentAPIClient.get_patient_appointments(patient_id)


def get_doctor_appointments(doctor_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get all appointments for a doctor"""
    return AppointmentAPIClient.get_doctor_appointments(doctor_id)