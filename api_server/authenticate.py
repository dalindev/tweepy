from app_config import LOGIN_TEMP_KEY
from flask import request, abort

def validate():
    auth_token = request.args.get("Authorization", None)
    if not auth_token or LOGIN_TEMP_KEY != auth_token:
        abort(401)
