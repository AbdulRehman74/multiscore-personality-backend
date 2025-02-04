from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.config import settings

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Retrieve user data using the access token
def get_user_data_from_token(token: str, db: Session):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError("Token does not contain 'sub' claim")
        
        # Fetch the user from the database
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise JWTError("User not found")
        
        return user
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")
