"""
Travel-specific endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.travel import TravelRequest, TravelResponse
from app.agents.travel_agent import TravelAgent
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/plan", response_model=TravelResponse)
async def plan_trip(
    request: TravelRequest,
    current_user = Depends(get_current_user)
):
    """Plan a complete trip"""
    agent = TravelAgent(current_user.id)
    
    task = {
        "destination": request.destination,
        "budget": request.budget,
        "dates": {
            "start": request.start_date,
            "end": request.end_date
        },
        "travelers": request.travelers,
        "preferences": request.preferences
    }
    
    result = await agent.execute(task)
    
    if result.get('status') == 'error':
        raise HTTPException(
            status_code=400,
            detail=result.get('error')
        )
    
    return result