import stripe
import os
from dotenv import load_dotenv
from app.core.auth import get_user_data_from_token
from app.core.database import get_db
from sqlalchemy.orm import Session

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Function to create or retrieve the Stripe customer ID
def create_stripe_customer(user, db: Session):
    if user.stripe_customer_id:
        return user.stripe_customer_id


    customer = stripe.Customer.create(
        email=user.email,
        name=user.full_name,
    )

    # Store the new customer ID in the database for future use
    user.stripe_customer_id = customer.id
    db.commit()

    return customer.id

# Function to create a payment intent
def create_payment_intent(amount: int, currency: str, payment_method: dict, token: str, db: Session):
    try:
        # Fetch user data from the access token
        user = get_user_data_from_token(token, db)

        # Create a Stripe customer if the user doesn't have one already
        stripe_customer_id = create_stripe_customer(user, db)

        # Extract payment method ID from the provided payment method object
        if 'id' not in payment_method:
            return {"error": "Payment method ID is missing", "status": "failed"}

        payment_method_id = payment_method['id']

        # Create the PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount * 100,  # Convert amount to cents
            currency=currency.lower(),
            payment_method=payment_method_id,
            customer=stripe_customer_id,
            confirm=True,
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never",  # Disables redirect-based payment methods
            }
        )

        # Return the payment intent details
        return {
            "payment_intent_id": payment_intent.id,
            "status": "success",
            "amount": amount,
            "currency": currency.upper()
        }

    except stripe.error.StripeError as e:
        return {
            "error": str(e),
            "status": "failed"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
