from APP.AI.medical_assitant import MedicalAssistantService
from APP.SCHEMAS.ai_schema import AIChatRequest, UserRole

def test_chat():
    assistant = MedicalAssistantService()

    request = AIChatRequest(
        user_id=1,
        role=UserRole.patient,
        session_id="test-session",
        message="What are symptoms of diabetes?",
        context=None
    )

    response = assistant.chat(request)

    print("\nAI RESPONSE:\n")
    print(response)

if __name__ == "__main__":
    test_chat()