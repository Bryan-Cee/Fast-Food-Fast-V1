import datetime
import os
import jwt
import psycopg2

from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from instance.config import app_configs

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
    admin = data.get('Admin')
    if not admin:
        admin = False
    hashed_pwd = generate_password_hash(data['password'], method='sha256')
    return Auth().create_user(username, hashed_pwd, admin)


@auth_bp.route('/login', methods=['POST'])
def login_user():
    authorization = request.authorization

    if not authorization or not authorization.username or not authorization.password:
        return make_response('Could not verify, please input all your credentials', 401,
                             {'WWW-Authenticate': 'Basic rearm="Login required"'})

    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, username, password FROM Users WHERE username = %s", (authorization.username,))
            user = cur.fetchone()

            if user is None:
                return make_response('Could not verify, user is not registred', 401,

                                     {'WWW-Authenticate': 'Basic rearm="Login required"'})

            if check_password_hash(user[2], authorization.password):
                token = jwt.encode({'user_id': user[0],
                                    'iat': datetime.datetime.now(),
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                                   "secret_to_encoding",
                                   algorithm='HS256')
                return jsonify({"Token": token.decode('UTF-8')})
            return make_response("wrong password", 401)
