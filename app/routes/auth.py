import json
from jsonschema import validate, ValidationError

from app.utils.response import json_response
from app.utils.jwt import create_token
from app.schemas.user import user_create_schema, user_login_schema
from app.services.user_service import create_user, get_user_by_email, verify_password

def register_auth_routes(app):
    @app.post("/signup")
    def signup(request):
        try:
            body = json.loads(request.body)
            validate(body, user_create_schema)
        except (json.JSONDecodeError, ValidationError) as e:
            return json_response({"error": str(e)}, 400)

        user = create_user(body["name"], body["email"], body["password"])
        if not user:
            return json_response({"error": "Email already exists"}, 409)
        
        token = create_token(user.id)
        return json_response({"token": token})

    @app.post("/login")
    def login(request):
        try:
            body = json.loads(request.body)
            validate(body, user_login_schema)
        except (json.JSONDecodeError, ValidationError) as e:
            return json_response({"error": str(e)}, 400)

        user = get_user_by_email(body["email"])
        if not user or not verify_password(user, body["password"]):
            return json_response({"error": "Invalid credentials"}, 401)

        token = create_token(user.id)
        return json_response({"token": token})
