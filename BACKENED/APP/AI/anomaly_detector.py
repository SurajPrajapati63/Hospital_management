# anomaly_detector.py

from ..SCHEMAS.ai_schema import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse
)


class AnomalyDetectionService:

    def detect(self, request: AnomalyDetectionRequest) -> AnomalyDetectionResponse:

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