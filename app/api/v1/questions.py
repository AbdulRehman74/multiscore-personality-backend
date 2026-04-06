import random
import json
import time
from fastapi import APIRouter
from app.models.question import Question

router = APIRouter()

with open("app/static/questions.json") as f:
    QUESTIONS = json.load(f)


@router.get("/questions")
async def get_questions():
    seed = int(time.time() * 1000)
    random.seed(seed)
    shuffled = random.sample(QUESTIONS, len(QUESTIONS))
    return {"seed": seed, "questions": shuffled}
