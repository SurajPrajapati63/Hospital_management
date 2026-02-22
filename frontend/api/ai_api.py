
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# Router
# ----------------------------
router = APIRouter()

# ----------------------------
# Pydantic Model for Request
# ----------------------------
class SymptomsRequest(BaseModel):
    symptoms: List[str]   # List of symptoms
    age: Optional[int] = None
    gender: Optional[str] = None

# ----------------------------
# Pydantic Model for Response
# ----------------------------
class PredictionResponse(BaseModel):
    probable_disease: str
    confidence: float
    recommended_action: str

# ----------------------------
# Dummy AI Model Function
# ----------------------------
def predict_disease(symptoms: List[str], age: Optional[int], gender: Optional[str]):
    """
    This is a placeholder AI function.
    Replace it with your real ML/DL model or API call.
    """
    # Example logic: very simple keyword matching
    if "fever" in symptoms and "cough" in symptoms:
        return {
            "probable_disease": "Flu",
            "confidence": 0.85,
            "recommended_action": "Take rest, drink fluids, and consult a doctor if severe."
        }
    elif "headache" in symptoms:
        return {
            "probable_disease": "Migraine",
            "confidence": 0.75,
            "recommended_action": "Avoid bright lights, rest, and take prescribed medication."
        }
    else:
        return {
            "probable_disease": "Unknown",
            "confidence": 0.50,
            "recommended_action": "Consult a doctor for proper diagnosis."
        }

# ----------------------------
# API Route
# ----------------------------
@router.post("/predict", response_model=PredictionResponse)
async def ai_predict(request: SymptomsRequest):
    prediction = predict_disease(request.symptoms, request.age, request.gender)
    return prediction