from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List

from app.schemas.ai_schema import (
    AIChatRequest,
    AIChatResponse,
    ReportSummaryRequest,
    ReportSummaryResponse,
    PrescriptionExplanationRequest,
    PrescriptionExplanationResponse,
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
    AnalyticsAIRequest,
    AnalyticsAIResponse,
    AIResponseType,
)

# from app.AI.report_summarizer import summarize_report
from app.AI.anomaly_detector import detect_anomalies

from app.AI.memory import save_memory_entry

router = APIRouter(prefix=".AI", tags=["AI"])


# ===============================
# 🤖 AI CHAT
# ===============================
@router.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(payload: AIChatRequest):
    try:
        result = await process_chat(payload)

        # Save conversation memory
        await save_memory_entry(
            session_id=payload.session_id,
            user_id=payload.user_id,
            message=payload.message,
            response=result["response"],
        )

        return AIChatResponse(
            response=result["response"],
            response_type=AIResponseType.chat,
            sources=result.get("sources"),
            confidence_score=result.get("confidence_score"),
            timestamp=datetime.utcnow().isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ===============================
# 📄 REPORT SUMMARY
# ===============================
@router.post("/summarize-report", response_model=ReportSummaryResponse)
async def summarize_lab_report(payload: ReportSummaryRequest):
    try:
        result = await summarize_report(payload.report_text, payload.role)

        return ReportSummaryResponse(
            summary=result["summary"],
            key_findings=result.get("key_findings"),
            risk_level=result.get("risk_level"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 💊 PRESCRIPTION EXPLANATION
# ===============================
@router.post("/explain-prescription", response_model=PrescriptionExplanationResponse)
async def explain_rx(payload: PrescriptionExplanationRequest):
    try:
        result = await explain_prescription(
            payload.prescription_text, payload.role
        )

        return PrescriptionExplanationResponse(
            explanation=result["explanation"],
            warnings=result.get("warnings"),
            side_effects=result.get("side_effects"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 🧪 ANOMALY DETECTION
# ===============================
@router.post("/detect-anomaly", response_model=AnomalyDetectionResponse)
async def anomaly_detection(payload: AnomalyDetectionRequest):
    try:
        result = await detect_anomalies(
            patient_id=payload.patient_id,
            lab_values=payload.lab_values,
        )

        return AnomalyDetectionResponse(
            anomalies_detected=result["anomalies_detected"],
            flagged_parameters=result.get("flagged_parameters"),
            severity_level=result.get("severity_level"),
            explanation=result.get("explanation"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 📊 ANALYTICS AI
# ===============================
@router.post("/analytics", response_model=AnalyticsAIResponse)
async def analytics_ai(payload: AnalyticsAIRequest):
    try:
        result = await generate_analytics(payload.query, payload.role)

        return AnalyticsAIResponse(
            answer=result["answer"],
            chart_data=result.get("chart_data"),
            insights=result.get("insights"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))