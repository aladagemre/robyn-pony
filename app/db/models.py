from pony.orm import Required
from app.db.database import db

class User(db.Entity):
    name = Required(str)
    email = Required(str, unique=True)
    password = Required(str)

db.generate_mapping(create_tables=True)
