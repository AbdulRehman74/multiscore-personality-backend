from pydantic import BaseModel
from typing import List, Dict, Optional

class Response(BaseModel):
    question_id: int
    answer: int

class ScoringRequest(BaseModel):
    responses: List[Response]
    seed: Optional[int] = None 

class ScoringResponse(BaseModel):
    scores: Dict[str, int]
    dominant_preferences: List[str]
    flag: str
    result_description: Optional[str] = None
    profile_type: Optional[str] = None
