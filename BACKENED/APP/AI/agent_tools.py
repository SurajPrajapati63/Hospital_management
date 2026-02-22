# agent_tools.py

from .medical_assitant import MedicalAssistantService
from .report_summarizer import ReportSummarizerService
from .prescription import PrescriptionService
from .anomaly_detector import AnomalyDetectionService


class AIAgent:

    def __init__(self):
        self.chat = MedicalAssistantService()
        self.summarizer = ReportSummarizerService()
        self.prescription = PrescriptionService()
        self.anomaly = AnomalyDetectionService()