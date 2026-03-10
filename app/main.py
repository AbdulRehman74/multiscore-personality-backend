import os
import uvicorn
import sentry_sdk

from fastapi import FastAPI
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware

from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.database import engine, SessionLocal, Base
from app.api.v1.auth import auth_router
from app.api.v1 import questions, scoring, decision_tree, payment, stripe_webhook
from app.core.config import configure_cors, settings
from app.admin import create_admin


# ----------------------------
# SENTRY INITIALIZATION
# ----------------------------
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    environment=settings.SENTRY_ENVIRONMENT,
    traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
    release=settings.SENTRY_RELEASE,
    send_default_pii=True,
)


# Create database tables
Base.metadata.create_all(bind=engine)


# FastAPI app
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-shdsfmcsdvjvcs3secret-admin-key"
)

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


# Debug route for testing Sentry
@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)