from pydantic import BaseModel

class Question(BaseModel):
    id: int
    text: str
    category: str
