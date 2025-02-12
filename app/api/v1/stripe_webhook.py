from fastapi.params import Depends
import stripe
import os
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
import logging

# Load webhook secret from environment variables
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/stripe_webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Webhook processing error")

    event_type = event["type"]
    payment_intent = event["data"]["object"]
    customer_id = payment_intent.get("customer")

    if not customer_id:
        return {"status": "ignored"}

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return {"status": "ignored"}

    if event_type == "payment_intent.succeeded":
        user.payment_status = "successful"
        user.version = "paid" 
        db.commit()
        return {"status": "user upgraded to paid"}

    elif event_type == "payment_intent.payment_failed":
        user.payment_status = "failed"
        db.commit()
        return {"status": "payment failed"}

    db.commit()
    return {"status": "webhook event not relevant"}
