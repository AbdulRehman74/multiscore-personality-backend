import json
import random
from typing import List, Dict
from collections import Counter
from app.models.scoring import Response
from app.core.utils import load_questions

ANSWER_SCORES = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5
}

CATEGORIES = ["Analytical", "Logistical", "Conceptual", "Relational"]

def calculate_scores(responses: List["Response"], seed: int = None) -> Dict[str, int]:
    questions = load_questions()

    # Recreate same random order shown to user
    if seed is not None:
        random.seed(seed)
        questions = random.sample(questions, len(questions))

    # Map by order index (so scoring follows same shuffled list)
    question_map = {q["id"]: q for q in questions}

    category_scores = {c: 0 for c in CATEGORIES}
    for r in responses:
        q = question_map.get(r.question_id)
        if not q:
            raise ValueError(f"Invalid question_id: {r.question_id}")
        answer_value = int(r.answer)
        if not (1 <= answer_value <= 5):
            raise ValueError("Answer must be between 1 and 5.")
        category_scores[q["category"]] += answer_value

    return category_scores



def determine_dominant_preferences(scores: Dict[str, int]) -> List[str]:
    preferred = [k for k, v in scores.items() if v >= 18]
    if not preferred:
        return []
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(preferred) == 3:
        if sorted_scores[2][1] <= sorted_scores[1][1] - 4 and sorted_scores[2][1] <= sorted_scores[0][1] - 4:
            return [sorted_scores[0][0], sorted_scores[1][0]]
    if len(preferred) == 4:
        if sorted_scores[3][1] >= 22:
            return [x[0] for x in sorted_scores]
        return [x[0] for x in sorted_scores[:3]]
    return preferred


def determine_flag(scores: Dict[str, int], responses: List["Response"]) -> str:
    values = list(scores.values())
    answer_counts = Counter([r.answer for r in responses])
    freq = Counter(values).most_common(1)[0][1]
    if len(set([r.answer for r in responses])) == 1:
        return "Uniform"
    if max(answer_counts.values()) >= 18:
        return "Low Variability"

    if all(v < 18 for v in values):
        return "No Preference"
    return ""
