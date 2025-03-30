from pony.orm import Database
from app.core.config import settings

db = Database()
db.bind(provider=settings.DB_PROVIDER, filename=settings.DB_NAME, create_db=True)
