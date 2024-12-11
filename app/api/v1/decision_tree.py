from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

# Input and output models
class DecisionTreeRequest(BaseModel):
    scores: Dict[str, int]

class DecisionTreeNode(BaseModel):
    category: str
    score: int
    is_dominant: bool

class DecisionTreeResponse(BaseModel):
    steps: List[DecisionTreeNode]
    outcome: str

OUTCOMES = [
    "Analytical",
    "Structural",
    "Conceptual",
    "Social",
    "Analytical/Structural",
    "Analytical/Conceptual",
    "Analytical/Social",
    "Structural/Conceptual",
    "Structural/Social",
    "Conceptual/Social",
    "Structural/Conceptual/Social",
    "Analytical/Conceptual/Social",
    "Analytical/Structural/Social",
    "Analytical/Structural/Conceptual",
    "Quadmodal",
]

def map_to_decision_tree(scores: Dict[str, int]) -> Dict:
    """
    Traverse the decision tree and return the steps and final outcome.
    """
    steps = []
    dominant_preferences = [category for category, score in scores.items() if score >= 7]

    # Add all categories and scores to the steps
    for category, score in scores.items():
        steps.append({
            "category": category,
            "score": score,
            "is_dominant": score >= 7
        })

    # Determine the outcome
    if len(dominant_preferences) == 4:
        outcome = "Quadmodal"
    elif len(dominant_preferences) == 1:
        outcome = dominant_preferences[0]
    elif len(dominant_preferences) > 1:
        outcome = "/".join(sorted(dominant_preferences))
    else:
        max_score = max(scores.values())
        highest_categories = [category for category, score in scores.items() if score == max_score]
        outcome = "/".join(sorted(highest_categories))

    return {"steps": steps, "outcome": outcome}

@router.post("/decision-tree", response_model=DecisionTreeResponse)
async def decision_tree(request: DecisionTreeRequest):
    try:
        decision_tree_data = map_to_decision_tree(request.scores)
        return DecisionTreeResponse(steps=decision_tree_data["steps"], outcome=decision_tree_data["outcome"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
