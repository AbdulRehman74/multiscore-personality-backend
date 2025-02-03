from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    email_verified = Column(Boolean, default=False)
    otp = Column(String)
    otp_expiry = Column(DateTime, default=datetime.utcnow)
    stripe_customer_id = Column(String, nullable=True)
