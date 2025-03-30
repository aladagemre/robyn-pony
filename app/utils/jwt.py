import os
from jose import jwt, JWTError

from ..core.config import settings



def create_token(user_id: int):
    return jwt.encode({"user_id": user_id}, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        return None
