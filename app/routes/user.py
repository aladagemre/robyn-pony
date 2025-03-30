from app.utils.jwt import decode_token
from app.utils.response import json_response
from app.services.user_service import get_user_by_id

def register_user_routes(app):
    @app.get("/me")
    def me(request):
        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Bearer "):
            return json_response({"error": "Token missing"}, 401)

        token = auth.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return json_response({"error": "Invalid token"}, 403)

        user = get_user_by_id(payload["user_id"])
        if not user:
            return json_response({"error": "User not found"}, 404)

        return json_response({"id": user.id, "name": user.name, "email": user.email})
