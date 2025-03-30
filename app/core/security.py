from jose import jwt, JWTError
from .config import settings

def create_token(data: dict):
    return jwt.encode(data, settings.JWT_SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        return None
