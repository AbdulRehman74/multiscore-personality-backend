import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import hash_password, verify_password, create_access_token
from app.core.email import send_otp_email, send_reset_link_email
from app.core.database import get_db
from app.models.user import User
from app.core.config import settings  # Import settings
from app.core.response import success_response, error_response
from datetime import datetime, timedelta
from app.models.basemodels import SignupRequest, VerifyOtpRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        return error_response("Email already registered")

    otp = str(random.randint(100000, 999999))
    hashed_password = hash_password(request.password)

    otp_expiry = datetime.utcnow() + timedelta(minutes=1)

    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name,
        otp=otp,
        otp_expiry=otp_expiry,
    )
    db.add(new_user)
    db.commit()

    send_otp_email(request.email, otp, request.full_name)
    return success_response("User registered. Please verify your email.")

@auth_router.post("/verify-otp")
def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return error_response("User not found")
    if user.otp != request.otp:
        return error_response("Invalid OTP")
    if user.otp_expiry and user.otp_expiry < datetime.utcnow():
        return error_response("OTP expired")

    user.email_verified = True
    user.otp = None
    user.otp_expiry = None
    db.commit()

    return success_response("Email verified successfully")

@auth_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        return error_response("Invalid credentials", status_code=401)
    if not user.email_verified:
        return error_response("Email not verified", status_code=403)

    access_token = create_access_token(data={"sub": user.email})
    return success_response("Login successful", {"access_token": access_token, "token_type": "bearer"})

@auth_router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return error_response("Email not registered", status_code=404)

    reset_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=15))
    reset_link = f"{settings.FRONTEND_DOMAIN}/reset-password?token={reset_token}"

    send_reset_link_email(user.email, reset_link, user.full_name)

    return success_response("Password reset link sent to your email.")

@auth_router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return error_response("Email not registered", status_code=404)

    user.hashed_password = hash_password(request.new_password)
    db.commit()

    return success_response("Password reset successfully")
