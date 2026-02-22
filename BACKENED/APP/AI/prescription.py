# prescription.py

from .llm_provider import LLMProvider
from ..schemas.ai_schema import (
    PrescriptionExplanationRequest,
    PrescriptionExplanationResponse
)


class PrescriptionService:

    def __init__(self):
        self.llm = LLMProvider()

    def explain(self, request: PrescriptionExplanationRequest) -> PrescriptionExplanationResponse:

        system_message = """
        You are a medical prescription explanation assistant.
        Explain clearly.
        Include warnings and side effects.
        """

        prompt = f"""
        Explain this prescription for a {request.role}:

        {request.prescription_text}
        """

        explanation = self.llm.generate_response(
            prompt=prompt,
            system_message=system_message
        )

        return PrescriptionExplanationResponse(
            explanation=explanation,
            warnings=["Consult doctor before stopping medication"],
            side_effects=["Nausea"]
        )