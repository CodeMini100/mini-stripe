import os
import logging
import jwt
from typing import Union, Optional
from datetime import datetime, timedelta
from jwt.exceptions import PyJWTError

logger = logging.getLogger(__name__)

# TODO: Replace default secret key with a secure key from environment or vault in production.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultsecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt(user_id: str) -> str:
    """
    Generates a JWT with user claims.

    Args:
        user_id (str): The ID of the user.

    Returns:
        str: The generated JWT string.
    """
    # TODO: Add additional payload claims as necessary.
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(token: str) -> Optional[dict]:
    """
    Validates and decodes a JWT.

    Args:
        token (str): The JWT string to decode.

    Returns:
        Optional[dict]: The decoded JWT payload if valid, otherwise None.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except PyJWTError as e:
        logger.error("JWT verification failed: %s", e)
        return None

# TODO: Implement session-based authentication if needed.