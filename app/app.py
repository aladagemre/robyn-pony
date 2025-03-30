from robyn import Robyn
from .routes.auth import register_auth_routes
from .routes.user import register_user_routes

app = Robyn(__file__)

# Register routes
register_auth_routes(app)
register_user_routes(app)


@app.get("/")
def home():
    return "Robyn Modular App with PonyORM and JWT"


if __name__ == "__main__":
    app.start(port=8000)
