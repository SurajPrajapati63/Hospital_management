"""
AI API Client Module
Handles all frontend HTTP requests to AI backend endpoints
"""

import requests
from typing import Dict, List, Any, Optional

# Backend API base URL
BASE_URL = "http://localhost:8000/api"
AI_ENDPOINT = f"{BASE_URL}/ai"


class AIAPIClient:
    """HTTP client for AI-related operations"""

    @staticmethod
    def predict_disease(symptoms: List[str], age: Optional[int] = None, gender: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Predict disease based on symptoms"""
        try:
            response = requests.post(
                f"{AI_ENDPOINT}/predict",
                json={"symptoms": symptoms, "age": age, "gender": gender},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error predicting disease: {str(e)}")
            return None

    @staticmethod
    def get_medical_recommendation(patient_id: str, condition: str) -> Optional[Dict[str, Any]]:
        """Get AI medical recommendations for a patient"""
        try:
            response = requests.post(
                f"{AI_ENDPOINT}/recommendation",
                json={"patient_id": patient_id, "condition": condition},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting recommendation: {str(e)}")
            return None

    @staticmethod
    def analyze_report(report_content: str) -> Optional[Dict[str, Any]]:
        """Analyze and summarize medical report"""
        try:
            response = requests.post(
                f"{AI_ENDPOINT}/analyze-report",
                json={"content": report_content},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error analyzing report: {str(e)}")
            return None

    @staticmethod
    def detect_anomaly(patient_id: str) -> Optional[Dict[str, Any]]:
        """Detect anomalies in patient health data"""
        try:
            response = requests.get(
                f"{AI_ENDPOINT}/anomaly/{patient_id}",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error detecting anomaly: {str(e)}")
            return None

    @staticmethod
    def chat_medical_assistant(message: str, patient_context: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Chat with AI medical assistant"""
        try:
            response = requests.post(
                f"{AI_ENDPOINT}/chat",
                json={"message": message, "patient_context": patient_context},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in medical assistant chat: {str(e)}")
            return None

    @staticmethod
    def generate_prescription_suggestion(symptoms: List[str], condition: str) -> Optional[Dict[str, Any]]:
        """Generate AI-suggested prescription based on symptoms"""
        try:
            response = requests.post(
                f"{AI_ENDPOINT}/prescription",
                json={"symptoms": symptoms, "condition": condition},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error generating prescription suggestion: {str(e)}")
            return None


# Convenience functions for direct use
def predict_disease(symptoms: List[str], age: Optional[int] = None, gender: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Predict disease based on symptoms"""
    return AIAPIClient.predict_disease(symptoms, age, gender)


def get_medical_recommendation(patient_id: str, condition: str) -> Optional[Dict[str, Any]]:
    """Get AI medical recommendations for a patient"""
    return AIAPIClient.get_medical_recommendation(patient_id, condition)


def analyze_report(report_content: str) -> Optional[Dict[str, Any]]:
    """Analyze and summarize medical report"""
    return AIAPIClient.analyze_report(report_content)


def detect_anomaly(patient_id: str) -> Optional[Dict[str, Any]]:
    """Detect anomalies in patient health data"""
    return AIAPIClient.detect_anomaly(patient_id)


def chat_medical_assistant(message: str, patient_context: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Chat with AI medical assistant"""
    return AIAPIClient.chat_medical_assistant(message, patient_context)


def generate_prescription_suggestion(symptoms: List[str], condition: str) -> Optional[Dict[str, Any]]:
    """Generate AI-suggested prescription based on symptoms"""
    return AIAPIClient.generate_prescription_suggestion(symptoms, condition)