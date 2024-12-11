import json
from app.core.config import settings


def load_questions():
    """Load questions from the JSON file."""
    with open(settings.QUESTIONS_FILE, "r") as file:
        return json.load(file)
