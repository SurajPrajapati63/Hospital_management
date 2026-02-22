"""
Analytics API Client Module
Handles all frontend HTTP requests to analytics backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
ANALYTICS_ENDPOINT = f"{BASE_URL}/analytics"


class AnalyticsAPIClient:
    """HTTP client for analytics-related operations"""

    @staticmethod
    def get_dashboard_overview() -> Optional[Dict[str, Any]]:
        """Get dashboard overview with key metrics"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/dashboard")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching dashboard overview: {str(e)}")
            return None

    @staticmethod
    def get_monthly_appointments() -> Optional[Dict[str, Any]]:
        """Get monthly appointment statistics"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/appointments/monthly")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching monthly appointments: {str(e)}")
            return None

    @staticmethod
    def get_monthly_revenue() -> Optional[Dict[str, Any]]:
        """Get monthly revenue statistics"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/revenue/monthly")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching monthly revenue: {str(e)}")
            return None

    @staticmethod
    def get_doctor_performance() -> Optional[List[Dict[str, Any]]]:
        """Get doctor performance metrics"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/doctors/performance")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching doctor performance: {str(e)}")
            return None

    @staticmethod
    def get_patient_growth() -> Optional[Dict[str, Any]]:
        """Get patient growth trends"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/patients/growth")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patient growth: {str(e)}")
            return None

    @staticmethod
    def get_outstanding_bills() -> Optional[Dict[str, Any]]:
        """Get outstanding bills summary"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/bills/outstanding")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching outstanding bills: {str(e)}")
            return None

    @staticmethod
    def generate_analytics_summary() -> Optional[Dict[str, Any]]:
        """Generate comprehensive analytics summary"""
        try:
            response = requests.get(f"{ANALYTICS_ENDPOINT}/summary")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error generating analytics summary: {str(e)}")
            return None


# Convenience functions for direct use
def get_dashboard_overview() -> Optional[Dict[str, Any]]:
    """Get dashboard overview with key metrics"""
    return AnalyticsAPIClient.get_dashboard_overview()


def get_monthly_appointments() -> Optional[Dict[str, Any]]:
    """Get monthly appointment statistics"""
    return AnalyticsAPIClient.get_monthly_appointments()


def get_monthly_revenue() -> Optional[Dict[str, Any]]:
    """Get monthly revenue statistics"""
    return AnalyticsAPIClient.get_monthly_revenue()


def get_doctor_performance() -> Optional[List[Dict[str, Any]]]:
    """Get doctor performance metrics"""
    return AnalyticsAPIClient.get_doctor_performance()


def get_patient_growth() -> Optional[Dict[str, Any]]:
    """Get patient growth trends"""
    return AnalyticsAPIClient.get_patient_growth()


def get_outstanding_bills() -> Optional[Dict[str, Any]]:
    """Get outstanding bills summary"""
    return AnalyticsAPIClient.get_outstanding_bills()


def generate_analytics_summary() -> Optional[Dict[str, Any]]:
    """Generate comprehensive analytics summary"""
    return AnalyticsAPIClient.generate_analytics_summary()
