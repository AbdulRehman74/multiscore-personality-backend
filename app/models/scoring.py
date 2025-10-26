from pydantic import BaseModel, Field, validator
from typing import List, Dict

class Response(BaseModel):
    question_id: int
    answer: int

class ScoringRequest(BaseModel):
    responses: List[Response] = Field(..., description="List of user responses for each question")
    seed: int = Field(..., description="Seed value used for consistent randomization of questions")

    @validator("responses")
    def validate_responses(cls, v):
        if not v or len(v) < 20:
            raise ValueError("At least 20 responses are required.")
        return v

    @validator("seed")
    def validate_seed(cls, v):
        if v is None:
            raise ValueError("Seed value is required.")
        return v

class ScoringResponse(BaseModel):
    scores: Dict[str, int]
    dominant_preferences: List[str]
    result_description: str | None = None
    profile_type: str | None = None
