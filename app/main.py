from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import select
from app.core.database import engine, SessionLocal
from app.api.v1.auth import auth_router
from app.api.v1 import questions, scoring, decision_tree, payment, stripe_webhook
from app.core.config import configure_cors
from app.core.database import Base, engine
from app.admin import create_admin

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

# Initialize Admin
admin = create_admin(app)

@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute(select(1))
