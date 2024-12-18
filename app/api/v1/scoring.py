from fastapi import APIRouter, HTTPException
from app.models.scoring import ScoringRequest, ScoringResponse
from app.core.scoring import calculate_scores, determine_dominant_preferences, determine_flag

router = APIRouter()


@router.post("/score", response_model=ScoringResponse)
async def score_responses(request: ScoringRequest):
    try:
        scores = calculate_scores(request.responses)
        dominant_preferences = determine_dominant_preferences(scores)
        flag = determine_flag(scores)
        return ScoringResponse(scores=scores, dominant_preferences=dominant_preferences, flag=flag)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))