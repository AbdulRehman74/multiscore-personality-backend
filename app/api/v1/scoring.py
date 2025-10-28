from fastapi import APIRouter, HTTPException
from app.models.scoring import ScoringRequest, ScoringResponse
from app.core.scoring import calculate_scores, determine_dominant_preferences, determine_flag
import json
import os

router = APIRouter()
RESULTS_PATH = os.path.join("app", "static", "results.json")

def build_response(success: bool, message: str, data: dict = None, case: str = None, details: str = None):
    body = {"success": success, "message": message}
    if case:
        body["case"] = case
    if details:
        body["details"] = details
    if data:
        body["data"] = data
    return body

@router.post("/score")
async def score_responses(request: ScoringRequest):
    try:
        scores = calculate_scores(request.responses, request.seed)
        flag = determine_flag(scores, request.responses)

        
        if flag == "Uniform":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="All your answers were the same.",
                    case="Uniform",
                    details="Your answers were all the same. To generate an accurate result, try responding more reflectively."
                )
            )

        if flag == "Low Variability":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="Your answers were too similar.",
                    case="Low Variability",
                    details="Your answers were almost all the same. To generate an accurate result, try responding more reflectively."
                )
            )

        if flag == "No Preference":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="We couldn’t find a clear result.",
                    case="No Preference",
                    details="You didn’t show a preference for a specific cognitive modality. To generate an accurate result, try responding more reflectively."
                )
            )


        # ---- Normal scoring ----
        dominant_preferences = determine_dominant_preferences(scores)
        if len(dominant_preferences) == 1:
            profile_type = "Unimodal"
        elif len(dominant_preferences) == 2:
            profile_type = "Dualmodal"
        elif len(dominant_preferences) == 3:
            profile_type = "Trimodal"
        elif len(dominant_preferences) == 4:
            profile_type = "Quadmodal"
        else:
            profile_type = None

        description = ""
        if dominant_preferences:
            with open(RESULTS_PATH, "r", encoding="utf-8") as f:
                result_data = json.load(f)

            possible_key = "/".join(sorted(dominant_preferences))
            result_key = None

            if possible_key in result_data:
                result_key = possible_key
            else:
                dominant_set = set(dominant_preferences)
                for key in result_data.keys():
                    if set(key.split("/")) == dominant_set:
                        result_key = key
                        break

            description = result_data.get(result_key, "") if result_key else ""

        return build_response(
            success=True,
            message="Score calculated successfully.",
            data={
                "scores": scores,
                "dominant_preferences": dominant_preferences,
                "profile_type": profile_type,
                "result_description": description
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=build_response(success=False, message=str(e))
        )
