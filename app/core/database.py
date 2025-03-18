from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

engine = create_engine("postgresql://postgres:evaw0wyGlOYEtW6zmuhs@msp-prod-db.cg1kmk40idam.us-east-1.rds.amazonaws.com:5432/postgres")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
