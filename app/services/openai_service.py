"""
OpenAI API service
"""
import openai
from typing import Dict, Any, List
from app.core.config import settings

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI()
    
    async def chat(self, prompt: str, context: List[Dict] = None) -> str:
        """Basic chat completion"""
        messages = context or []
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def structured_response(self, prompt: str, schema: Dict = None) -> Dict:
        """Get structured JSON response"""
        if schema:
            prompt += f"\n\nReturn JSON matching schema: {schema}"
        
        response = await self.chat(prompt)
        
        # Parse JSON from response
        import json
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            return {"raw_response": response}
    
    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment and intent"""
        prompt = f"""
        Analyze: "{text}"
        
        Return JSON with:
        - sentiment (positive/negative/neutral)
        - urgency (high/medium/low)
        - intent (book, inquire, cancel, etc.)
        - key_details (extracted entities)
        """
        return await self.structured_response(prompt)