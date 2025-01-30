import json
from app.core.config import settings
from dotenv import load_dotenv
import os


load_dotenv()


def load_questions():
    """Load questions from the JSON file."""
    with open(settings.QUESTIONS_FILE, "r") as file:
        return json.load(file)

