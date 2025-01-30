from fastapi import FastAPI
from app.api.v1.auth import auth_router
from app.api.v1 import questions, scoring, decision_tree
from app.core.config import configure_cors
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Set up CORS middleware
configure_cors(app)

# Include 
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")
app.include_router(decision_tree.router, prefix="/api/v1")
