from robyn import Robyn
from app.routes.auth import register_auth_routes
from app.routes.user import register_user_routes

app = Robyn(__file__)

# Register routes
register_auth_routes(app)
register_user_routes(app)

if __name__ == "__main__":
    app.start(port=8000)
