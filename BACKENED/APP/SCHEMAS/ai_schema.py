from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# =========================
# ENUMS
# =========================

class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"


class AIResponseType(str, Enum):
    chat = "chat"
    summary = "summary"
    explanation = "explanation"
    anomaly = "anomaly"
    analytics = "analytics"


# =========================
# SAFETY
# =========================

class AISafetyMeta(BaseModel):
    restricted_content: bool
    reason: Optional[str] = None


# =========================
# CHAT
# =========================

class AIChatRequest(BaseModel):
    user_id: int
    role: UserRole
    session_id: Optional[str] = None
    message: str = Field(..., min_length=2)
    context: Optional[Dict[str, Any]] = None


class AIChatResponse(BaseModel):
    response: str
    response_type: AIResponseType
    safety: Optional[AISafetyMeta] = None
    sources: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    timestamp: Optional[str] = None


class AIStreamChunk(BaseModel):
    chunk: str
    done: bool


# =========================
# RAG
# =========================

class RAGSource(BaseModel):
    document_name: str
    page_number: Optional[int] = None
    snippet: str
    score: float


# =========================
# REPORT SUMMARY
# =========================

class ReportSummaryRequest(BaseModel):
    report_text: str
    role: UserRole


class ReportSummaryResponse(BaseModel):
    summary: str
    key_findings: Optional[List[str]] = None
    risk_level: Optional[str] = None


# =========================
# PRESCRIPTION EXPLANATION
# =========================

class PrescriptionExplanationRequest(BaseModel):
    prescription_text: str
    role: UserRole


class PrescriptionExplanationResponse(BaseModel):
    explanation: str
    warnings: Optional[List[str]] = None
    side_effects: Optional[List[str]] = None


# =========================
# ANOMALY DETECTION
# =========================

class AnomalyDetectionRequest(BaseModel):
    patient_id: int
    lab_values: Dict[str, float]


class AnomalyDetectionResponse(BaseModel):
    anomalies_detected: bool
    flagged_parameters: Optional[List[str]] = None
    severity_level: Optional[str] = None
    explanation: Optional[str] = None


# =========================
# ANALYTICS AI
# =========================

class AnalyticsAIRequest(BaseModel):
    query: str
    role: UserRole


class AnalyticsAIResponse(BaseModel):
    answer: str
    chart_data: Optional[Dict[str, Any]] = None
    insights: Optional[List[str]] = None


# =========================
# MEMORY
# =========================

class AIMemoryEntry(BaseModel):
    session_id: str
    user_id: int
    message: str
    response: str
    timestamp: str