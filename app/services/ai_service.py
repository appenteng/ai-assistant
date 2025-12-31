"""
AI Service - Basic version
"""
class AIService:
    def __init__(self):
        self.responses = {
            "hello": "Hi! I'm your AI assistant.",
            "travel": "I can help plan trips!",
            "help": "Ask me anything!"
        }

    def chat(self, message: str) -> str:
        """Simple chat response"""
        msg_lower = message.lower()
        for key, response in self.responses.items():
            if key in msg_lower:
                return response
        return f"I heard: '{message}'. How can I help?"

    def analyze(self, text: str) -> dict:
        """Simple sentiment analysis"""
        return {
            "text": text,
            "sentiment": "positive",
            "confidence": 0.8
        }
