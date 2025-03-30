from pony.orm import db_session
from app.db.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@db_session
def create_user(name, email, password):
    if User.get(email=email):
        return None
    return User(name=name, email=email, password=generate_password_hash(password))

@db_session
def get_user_by_email(email):
    return User.get(email=email)

@db_session
def get_user_by_id(user_id):
    return User.get(id=user_id)

@db_session
def verify_password(user, password):
    return check_password_hash(user.password, password)
