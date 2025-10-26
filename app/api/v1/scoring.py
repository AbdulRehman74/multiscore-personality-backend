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

        # ---- Handle all invalid test patterns as errors ----
        if flag == "Uniform":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="Invalid response pattern detected.",
                    case="Uniform",
                    details="All answers were identical. Please retake the test with varied responses."
                )
            )

        if flag == "Low Variability":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="Invalid response pattern detected.",
                    case="Low Variability",
                    details="Too many answers were the same (≥18 identical). Please provide more varied responses."
                )
            )

        if flag == "No Preference":
            raise HTTPException(
                status_code=400,
                detail=build_response(
                    success=False,
                    message="Invalid response pattern detected.",
                    case="No Preference",
                    details="No clear preference was found. All category scores were below the threshold of 18."
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
