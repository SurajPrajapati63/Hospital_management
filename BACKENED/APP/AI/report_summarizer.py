# report_summarizer.py

from .llm_provider import LLMProvider
from app.schemas.ai_schema import (
    ReportSummaryRequest,
    ReportSummaryResponse
)


class ReportSummarizerService:

    def __init__(self):
        self.llm = LLMProvider()

    def summarize(self, request: ReportSummaryRequest) -> ReportSummaryResponse:

        system_message = """
        You are a medical report summarization AI.
        Extract key findings and assess risk level.
        """

        prompt = f"""
        Summarize this medical report for a {request.role}:

        {request.report_text}
        """

        summary = self.llm.generate_response(
            prompt=prompt,
            system_message=system_message
        )

        return ReportSummaryResponse(
            summary=summary,
            key_findings=["Auto-detected finding 1"],
            risk_level="Medium"
        )