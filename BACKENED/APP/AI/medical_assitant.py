# medical_assistant.py

from datetime import datetime
from .llm_provider import LLMProvider
from .memory import AIMemoryStore
from ..schemas.ai_schema import (
    AIChatRequest,
    AIChatResponse,
    AIResponseType,
    AISafetyMeta,
    AIMemoryEntry
)


class MedicalAssistantService:

    def __init__(self):
        self.llm = LLMProvider()
        self.memory_store = AIMemoryStore()

    def _build_system_prompt(self, role: str) -> str:
        """
        Role-based medical instruction
        """

        base_prompt = """
        You are a professional hospital AI assistant.
        Provide medically safe, evidence-based information.
        If unsure, advise consulting a licensed doctor.
        Never provide dangerous medical instructions.
        """

        if role == "doctor":
            return base_prompt + "\nProvide clinically detailed explanations."
        elif role == "patient":
            return base_prompt + "\nExplain in simple, easy-to-understand language."
        elif role == "admin":
            return base_prompt + "\nFocus on hospital analytics and operational insights."

        return base_prompt

    def chat(self, request: AIChatRequest) -> AIChatResponse:

        # Retrieve memory (if session exists)
        previous_conversation = []
        if request.session_id:
            previous_conversation = self.memory_store.get_session_memory(request.session_id)

        conversation_context = "\n".join(
            [f"User: {m.message}\nAI: {m.response}" for m in previous_conversation]
        )

        system_prompt = self._build_system_prompt(request.role)

        final_prompt = f"""
        Previous Conversation:
        {conversation_context}

        Current Message:
        {request.message}

        Additional Context:
        {request.context}
        """

        ai_text = self.llm.generate_response(
            prompt=final_prompt,
            system_message=system_prompt,
            temperature=0.3
        )

        # Save memory
        if request.session_id:
            self.memory_store.add_entry(
                AIMemoryEntry(
                    session_id=request.session_id,
                    user_id=request.user_id,
                    message=request.message,
                    response=ai_text,
                    timestamp=str(datetime.utcnow())
                )
            )

        # Simple safety check
        restricted = False
        reason = None

        dangerous_keywords = ["suicide", "kill", "overdose"]

        if any(word in request.message.lower() for word in dangerous_keywords):
            restricted = True
            reason = "Potentially harmful medical content detected."

        return AIChatResponse(
            response=ai_text,
            response_type=AIResponseType.chat,
            safety=AISafetyMeta(
                restricted_content=restricted,
                reason=reason
            ),
            confidence_score=0.93,
            timestamp=str(datetime.utcnow())
        )