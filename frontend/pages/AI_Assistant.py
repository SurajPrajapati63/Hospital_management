
from typing import List, Dict
from datetime import datetime

# ----------------------------
# Dummy AI Knowledge Base
# ----------------------------
AI_KNOWLEDGE_BASE: Dict[str, Dict] = {
    "fever": {
        "disease": "Flu",
        "confidence": 0.85,
        "recommendation": "Take rest, drink fluids, monitor temperature, consult doctor if high fever persists."
    },
    "cough": {
        "disease": "Common Cold",
        "confidence": 0.80,
        "recommendation": "Drink warm fluids, avoid cold drinks, take cough syrup if needed."
    },
    "headache": {
        "disease": "Migraine",
        "confidence": 0.75,
        "recommendation": "Rest in a quiet dark room, hydrate well, take prescribed medication if necessary."
    },
    "chest pain": {
        "disease": "Heart Problem",
        "confidence": 0.90,
        "recommendation": "Seek emergency medical attention immediately."
    },
}

# ----------------------------
# AI Prediction Function
# ----------------------------
def analyze_symptoms(symptoms: List[str], age: int = None, gender: str = None) -> Dict:
    """
    Analyze symptoms and return probable disease, confidence, and recommendations.
    This is a simple rule-based AI. Replace with ML/DL model for real predictions.
    """
    result = {"probable_disease": "Unknown", "confidence": 0.50, "recommended_action": "Consult a doctor."}

    for symptom in symptoms:
        key = symptom.lower()
        if key in AI_KNOWLEDGE_BASE:
            result["probable_disease"] = AI_KNOWLEDGE_BASE[key]["disease"]
            result["confidence"] = AI_KNOWLEDGE_BASE[key]["confidence"]
            result["recommended_action"] = AI_KNOWLEDGE_BASE[key]["recommendation"]
            break  # Return first match

    # Optionally, add age/gender adjustments (example)
    if age and age > 60:
        result["recommended_action"] += " Elderly patients should consult a doctor promptly."

    return result


# ----------------------------
# AI Chat Helper Function
# ----------------------------
def chat_with_ai(message: str) -> str:
    """
    Simple chat logic: respond based on keywords in the message.
    Can be integrated with chat_ui.py
    """
    msg = message.lower()
    for key in AI_KNOWLEDGE_BASE.keys():
        if key in msg:
            return f"AI Response: {AI_KNOWLEDGE_BASE[key]['recommendation']} (Disease: {AI_KNOWLEDGE_BASE[key]['disease']})"
    
    return "AI Response: I need more details to provide advice. Can you describe your symptoms further?"


# ----------------------------
# Example Usage
# ----------------------------
if __name__ == "__main__":
    # Example 1: Symptom analysis
    symptoms_list = ["fever", "cough"]
    prediction = analyze_symptoms(symptoms_list, age=25, gender="male")
    print("Prediction:", prediction)

    # Example 2: Chat response
    user_message = "I have a headache since morning."
    response = chat_with_ai(user_message)
    print("Chat AI:", response)