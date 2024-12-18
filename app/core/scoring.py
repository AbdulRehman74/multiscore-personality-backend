import json
from typing import List, Dict
from app.models.scoring import Response
from app.core.utils import load_questions


ANSWER_SCORES = {"Agree": 3, "Neutral": 2, "Disagree": 1}


def calculate_scores(responses: List["Response"]) -> Dict[str, int]:
    """Calculate scores for each category based on user responses."""
    questions = load_questions()
    category_scores = {category: 0 for category in {"Analytical", "Structural", "Conceptual", "Social"}}

    for response in responses:
        question = next((q for q in questions if q["id"] == response.question_id), None)
        if not question:
            raise ValueError(f"Invalid question_id: {response.question_id}")
        category = question["category"]
        score = ANSWER_SCORES.get(response.answer, 0)
        category_scores[category] += score

    return category_scores


def determine_dominant_preferences(scores: Dict[str, int]) -> List[str]:
    """Determine dominant preferences based on scores."""
    dominant_preferences = [cat for cat, score in scores.items() if score >= 7]

    if not dominant_preferences:
        max_score = max(scores.values())
        dominant_preferences = [cat for cat, score in scores.items() if score == max_score]

    return dominant_preferences

def determine_flag(scores: Dict[str, int]) -> str:
    unique_scores = set(scores.values())
    if unique_scores == {9}:
        return "Agree"
    elif unique_scores == {3}:
        return "Disagree"
    elif unique_scores == {6}:
        return "Neutral"
    return ""