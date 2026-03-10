import os
import uvicorn
import sentry_sdk

from fastapi import FastAPI, Header, HTTPException
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
if settings.SENTRY_DSN:
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


# ----------------------------
# CREATE DATABASE TABLES
# ----------------------------
Base.metadata.create_all(bind=engine)


# ----------------------------
# FASTAPI APP
# ----------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)


# ----------------------------
# MIDDLEWARE
# ----------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)

configure_cors(app)


# ----------------------------
# ROUTERS
# ----------------------------
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")
app.include_router(decision_tree.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1/payment")
app.include_router(stripe_webhook.router, prefix="/api/v1")


# ----------------------------
# ADMIN PANEL
# ----------------------------
admin = create_admin(app)


# ----------------------------
# ROOT ENDPOINT
# ----------------------------
@app.get("/")
def root():
    return {"message": "API is running"}


# ----------------------------
# STARTUP DB CHECK
# ----------------------------
@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute(select(1))


# ----------------------------
# SAFE SENTRY TEST ENDPOINT
# ----------------------------
@app.get("/internal/sentry-test")
async def sentry_test(x_debug_token: str = Header(None)):
    """
    Secure endpoint to trigger Sentry errors.
    Only accessible if correct debug token is provided.
    """
    if settings.SENTRY_ENVIRONMENT == "production":
        if x_debug_token != settings.SECRET_KEY:
            raise HTTPException(status_code=403, detail="Forbidden")

    raise RuntimeError("Sentry test exception triggered")


# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
    )