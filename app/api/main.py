from fastapi import APIRouter
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.get("/test")
def test_endpoint():
    return {"message": "API is working!"}

@router.post("/chat")
def chat_with_ai(message: str):
    response = ai_service.chat(message)
    return {"ai_response": response}