from pydantic import BaseModel
from typing import List, Dict


class Response(BaseModel):
    question_id: int
    answer: str  # "Agree", "Neutral", "Disagree"


class ScoringRequest(BaseModel):
    responses: List[Response]


class ScoringResponse(BaseModel):
    scores: Dict[str, int]
    dominant_preferences: List[str]
