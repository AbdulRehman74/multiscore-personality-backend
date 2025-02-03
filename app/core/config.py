import os
from os import environ
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware


class Settings(BaseSettings):
    APP_NAME: str = "Multiscore Personality App"
    VERSION: str = "1.0.0"
    QUESTIONS_FILE: str
    SENDGRID_API_KEY: str  
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FRONTEND_DOMAIN: str
    STRIPE_SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
