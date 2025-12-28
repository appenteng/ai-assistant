"""
General helper functions
"""
import json
from typing import Any, Dict
from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime for API response"""
    return dt.isoformat() if dt else None

def safe_json_loads(data: str) -> Dict:
    """Safely load JSON"""
    try:
        return json.loads(data)
    except:
        return {}

def extract_entities(text: str) -> Dict[str, Any]:
    """Extract entities from text (simplified)"""
    # In production, use NLP library
    return {"text": text, "entities": []}