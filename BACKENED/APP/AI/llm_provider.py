import google.generativeai as genai
from APP.config import settings


class LLMProvider:

    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_response(
        self,
        prompt: str,
        system_message: str,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:

        try:
            # Gemini does not use system/user roles like OpenAI
            # So we merge system + user into one structured prompt

            full_prompt = f"""
{system_message}

User:
{prompt}
"""

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
            )

            return response.text.strip()

        except Exception as e:
            return f"Error: {str(e)}"