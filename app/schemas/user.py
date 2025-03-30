user_create_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string", "minLength": 6}
    },
    "required": ["name", "email", "password"]
}

user_login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["email", "password"]
}
