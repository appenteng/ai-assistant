# app/services/ai_service.py - ENHANCED VERSION
import random
from typing import Dict, List

class AIService:
    def __init__(self):
        self.responses = {
            "greeting": ["Hello! I'm your AI assistant.", "Hi there!", "Hey! What can I do?"],
            "travel": ["I can help plan trips!", "Let's plan your next adventure!", "Travel planning is my specialty!"],
            "help": ["I can: 1) Travel planning 2) Task automation 3) Schedule management"],
            "unknown": ["I'm great at planning trips!", "Try asking about travel!"]
        }
    
    def chat(self, message: str) -> str:
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["greeting"])
        elif any(word in message_lower for word in ["travel", "trip", "vacation"]):
            return random.choice(self.responses["travel"])
        elif any(word in message_lower for word in ["help", "what can you do"]):
            return random.choice(self.responses["help"])
        else:
            return random.choice(self.responses["unknown"])
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "happy", "awesome"]
        negative_words = ["bad", "terrible", "awful", "hate", "angry"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        total_words = len(text_lower.split())
        
        if total_words == 0:
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.0}
        
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        neutral_score = 1 - positive_score - negative_score
        
        return {
            "positive": round(positive_score, 2),
            "negative": round(negative_score, 2),
            "neutral": round(max(neutral_score, 0), 2)
        }