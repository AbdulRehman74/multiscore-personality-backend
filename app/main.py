import os
import uvicorn
from fastapi import FastAPI
from sqlalchemy import select

from app.core.database import engine, SessionLocal, Base
from app.api.v1.auth import auth_router
from app.api.v1 import questions, scoring, decision_tree, payment, stripe_webhook
from app.core.config import configure_cors
from app.admin import create_admin

Base.metadata.create_all(bind=engine)

app = FastAPI()

configure_cors(app)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")
app.include_router(decision_tree.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1/payment")
app.include_router(stripe_webhook.router, prefix="/api/v1")

admin = create_admin(app)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute(select(1))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)