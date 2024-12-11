from fastapi import APIRouter
from app.models.question import Question
from typing import List
import json

router = APIRouter()

# Load questions from the static JSON file
with open("app/static/questions.json") as f:
    QUESTIONS = json.load(f)

@router.get("/questions", response_model=List[Question])
async def get_questions():
    """Return the fixed set of questions."""
    return QUESTIONS
