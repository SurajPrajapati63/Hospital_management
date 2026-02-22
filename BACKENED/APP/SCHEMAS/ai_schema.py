from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


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

class AIChatRequest(BaseModel):
    user_id: int
    role: UserRole
    session_id: Optional[str] = None
    message: str = Field(..., min_length=2)
    context: Optional[Dict[str, Any]] = None  # optional metadata

class AIChatResponse(BaseModel):
    response: str
    response_type: AIResponseType
    sources: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    timestamp: Optional[str] = None

class RAGSource(BaseModel):
    document_name: str
    page_number: Optional[int]
    snippet: str
    score: float

class ReportSummaryRequest(BaseModel):
    report_text: str
    role: UserRole


class ReportSummaryResponse(BaseModel):
    summary: str
    key_findings: Optional[List[str]]
    risk_level: Optional[str]

class PrescriptionExplanationRequest(BaseModel):
    prescription_text: str
    role: UserRole


class PrescriptionExplanationResponse(BaseModel):
    explanation: str
    warnings: Optional[List[str]]
    side_effects: Optional[List[str]]

class AnomalyDetectionRequest(BaseModel):
    patient_id: int
    lab_values: Dict[str, float]


class AnomalyDetectionResponse(BaseModel):
    anomalies_detected: bool
    flagged_parameters: Optional[List[str]]
    severity_level: Optional[str]
    explanation: Optional[str]

class AnalyticsAIRequest(BaseModel):
    query: str
    role: UserRole


class AnalyticsAIResponse(BaseModel):
    answer: str
    chart_data: Optional[Dict[str, Any]]
    insights: Optional[List[str]]

class AIMemoryEntry(BaseModel):
    session_id: str
    user_id: int
    message: str
    response: str
    timestamp: str

class AISafetyMeta(BaseModel):
    restricted_content: bool
    reason: Optional[str]

class AIChatResponse(BaseModel):
    response: str
    response_type: AIResponseType
    safety: Optional[AISafetyMeta]
    sources: Optional[List[str]]
    confidence_score: Optional[float]
    timestamp: Optional[str]

class AIStreamChunk(BaseModel):
    chunk: str
    done: bool