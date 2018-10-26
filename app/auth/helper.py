from functools import wraps
import jwt
import os
from flask import request, make_response, jsonify
import psycopg2
import psycopg2.extras
from instance.config import app_configs
from app.users.models import conn

env = app_configs[os.getenv('APP_SETTINGS')]


def token_require(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token or 'x-access-token' == "undefined":
            return make_response(jsonify({"status": "failed", "message": "Token is missing, please login"}), 401)
        try:
            data = jwt.decode(token, env.SECRET_KEY, algorithms='HS256')
            user_id = data.get('user_id')
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT user_id, admin FROM Users WHERE user_id = %s", (user_id,))
                    current_user = cur.fetchone()
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"status": "failed",
                                          "message": "Token has expired Please login again"}), 401)
        except Exception as err:
            return err
        return func(current_user, *args, **kwargs)
    return decorated_func
