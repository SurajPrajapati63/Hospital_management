# anomaly_detector.py

from ..schemas.ai_schema import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse
)


class AnomalyDetectionService:

    def detect_anomaly(self, data: dict) -> dict:
        """Detect anomalies in patient data"""
        try:
            lab_values = data.get("lab_values", {})
            flagged = []

            for key, value in lab_values.items():
                if isinstance(value, (int, float)) and value > 100:  # example threshold
                    flagged.append(key)

            return {
                "anomaly_detected": len(flagged) > 0,
                "flagged_parameters": flagged,
                "severity_level": "High" if flagged else "Normal",
                "confidence_score": 0.85,
                "details": "Some lab values exceed normal threshold." if flagged else "All values within normal range.",
            }
        except Exception as e:
            return {
                "anomaly_detected": False,
                "flagged_parameters": [],
                "severity_level": "Unknown",
                "confidence_score": 0.0,
                "details": f"Error detecting anomalies: {str(e)}",
            }

    def detect(self, request: AnomalyDetectionRequest) -> AnomalyDetectionResponse:
        """Legacy method for schema compatibility"""
        flagged = []

        for key, value in request.lab_values.items():
            if value > 100:   # example threshold
                flagged.append(key)

        return AnomalyDetectionResponse(
            anomalies_detected=len(flagged) > 0,
            flagged_parameters=flagged,
            severity_level="High" if flagged else "Normal",
            explanation="Some lab values exceed normal threshold."
        )