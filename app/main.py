from fastapi import FastAPI
from app.api.v1 import questions, scoring, decision_tree
from app.core.config import configure_cors

app = FastAPI()

configure_cors(app)

# Include routers
app.include_router(questions.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")
app.include_router(decision_tree.router, prefix="/api/v1")
