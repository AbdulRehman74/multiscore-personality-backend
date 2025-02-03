from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict
from app.core.stripe_service import create_payment_intent
from app.core.auth import get_user_data_from_token
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: int
    currency: str
    payment_method: Dict  # Expecting the entire payment method object

# Dependency to extract token from headers
def get_token(authorization: str = Header(...)):
    # Assuming token is passed in the format 'Bearer <token>'
    token = authorization.split(" ")[1] if " " in authorization else None
    if not token:
        raise HTTPException(status_code=403, detail="Token missing or invalid")
    return token    

@router.post("/create-payment-intent/")
async def create_payment(request: PaymentRequest, token: str = Depends(get_token), db: Session = Depends(get_db)):
    response = create_payment_intent(request.amount, request.currency, request.payment_method, token, db)
    if response["status"] == "failed":
        raise HTTPException(status_code=400, detail=response["error"])
    return response
