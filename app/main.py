from fastapi import FastAPI
from app.api.v1.auth import auth_router
from app.api.v1 import questions, scoring, decision_tree, payment, stripe_webhook
from app.core.config import configure_cors
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI()

# CORS configuration
configure_cors(app)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")
app.include_router(decision_tree.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1/payment")
app.include_router(stripe_webhook.router, prefix="/api/v1")
