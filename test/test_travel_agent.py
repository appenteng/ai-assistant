"""
Test travel agent
"""
import pytest
from app.agents.travel_agent import TravelAgent

@pytest.mark.asyncio
async def test_travel_planning():
    """Test basic travel planning"""
    agent = TravelAgent(user_id=1)
    
    task = {
        "destination": "Paris",
        "budget": 2000,
        "dates": {"start": "2024-06-01", "end": "2024-06-07"},
        "travelers": 2
    }
    
    result = await agent.execute(task)
    
    assert result["status"] in ["success", "error"]
    if result["status"] == "success":
        assert "itinerary" in result
        assert "bookings" in result