import datetime
import os
import jwt
import psycopg2

from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import check_password_hash
from instance.config import app_configs
import psycopg2.extras
from ..users.models import conn as connection

env = os.getenv('APP_SETTINGS')
config = app_configs[env]

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v2/auth')

conn = psycopg2.connect(host="localhost",
                        database=config.DBNAME,
                        user=config.USER,
                        password=config.PASSWORD)


@auth_bp.route('/signup', methods=['POST'])
def user_login():
    from .models import Auth
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    return Auth().create_user(username, password, email)


@auth_bp.route('/login', methods=['POST'])
def login_user():
    authorization = request.authorization

    if not authorization or not authorization.username or not authorization.password:
        return make_response(jsonify({"status": "Failed",
                                      "message": "Could not verify, please input all your credentials"}), 403,
                             {'WWW-Authenticate': 'Basic rearm="Login required"'})

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT user_id, username, password FROM Users WHERE username = %s", (authorization.username,))
            user = cur.fetchone()

            if user is None:
                return make_response(jsonify(
                    {"status": "Failed",
                     "message": "Could not verify, invalid credentials check your username or password"}), 403,
                    {'WWW-Authenticate': 'Basic rearm="Login required"'})

            if check_password_hash(user['password'], authorization.password):
                token = jwt.encode({'user_id': user['user_id'],
                                    'iat': datetime.datetime.now(),
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                                   config.SECRET_KEY,
                                   algorithm='HS256')
                return jsonify({"status": "Success", "Token": token.decode('UTF-8')})
            return make_response(jsonify({
                "status": "Failed",
                          "message": "Could not verify, invalid credentials check your username or password"}), 403,
                                 {'WWW-Authenticate': 'Basic rearm="Login required"'})
