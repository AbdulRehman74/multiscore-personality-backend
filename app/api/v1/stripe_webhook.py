from fastapi.params import Depends
import stripe
import os
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

# Load webhook secret from environment variables
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter()

@router.post("/stripe_webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    print("Webhook received")

    try:
        print("Constructing event")
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        print("Invalid signature in Stripe webhook")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        print(f"Webhook processing error: {e}")
        raise HTTPException(status_code=400, detail="Webhook processing error")

    event_type = event["type"]
    print(f"Event type: {event_type}")

    payment_intent = event["data"]["object"]
    customer_id = payment_intent.get("customer")

    if not customer_id:
        print(f"Webhook received event {event_type} without a customer ID.")
        return {"status": "ignored"}

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        print(f"No user found for Stripe customer ID: {customer_id}")
        return {"status": "ignored"}

    if event_type == "payment_intent.succeeded":
        user.payment_status = "successful"
        print(f"Payment successful for user: {user.email}")
        db.commit()
        return {"status": "webhook handled successfully"}
    
    elif event_type == "payment_intent.payment_failed":
        user.payment_status = "failed"
        print(f"Payment failed for user: {user.email}")
        db.commit()
        return {"status": "webhook failed"}

    db.commit()
    return {"status": "webhook not handled"}
