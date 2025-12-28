# app/api/chat.py
from fastapi import APIRouter
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.get("/")
def chat(message: str = "Hello"):
    """Chat with AI"""
    response = ai_service.chat(message)
    sentiment = ai_service.analyze_sentiment(message)

    return {
        "message": message,
        "response": response,
        "sentiment": sentiment
    }


@router.get("/sentiment")
def analyze_sentiment(text: str):
    """Analyze text sentiment"""
    sentiment = ai_service.analyze_sentiment(text)
    return {
        "text": text,
        "sentiment": sentiment
    }