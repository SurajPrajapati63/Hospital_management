# rag_engine.py

from .llm_provider import LLMProvider
from ..schemas.ai_schema import RAGSource


class RAGEngine:

    def __init__(self):
        self.llm = LLMProvider()

    def query(self, question: str):

        sources = [
            RAGSource(
                document_name="cardiology_guidelines.pdf",
                page_number=12,
                snippet="Hypertension treatment includes ACE inhibitors...",
                score=0.87
            )
        ]

        context = "\n".join([s.snippet for s in sources])

        system_message = """
        You are a hospital knowledge assistant.
        Answer ONLY using provided context.
        """

        prompt = f"""
        Context:
        {context}

        Question:
        {question}
        """

        answer = self.llm.generate_response(
            prompt=prompt,
            system_message=system_message
        )

        return answer, sources