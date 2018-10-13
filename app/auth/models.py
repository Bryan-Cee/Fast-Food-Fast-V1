import os

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
from instance.config import app_configs
from validator import credentials_checker
from app.users.models import conn as connection

env = os.getenv('APP_SETTINGS')
config = app_configs[env]


class Auth:

    def __init__(self):
        self.conn = connection

    def create_user(self, username, password, email):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM Users WHERE email = %s", (email,))
                checks = cur.fetchone()
                if not username or not password or not email:
                    prompt = {
                        "status": "failed",
                        "message": "Enter all the required data correctly"
                    }
                    return make_response(jsonify(prompt)), 409
                result = credentials_checker(username, password, email)
                messages = ('Enter only alphabetic characters for your username',
                            'Enter a password longer than 6 characters',
                            'Password must have atleast one lowercase one upper case and one digit',
                            'Enter the correct format of the email e.g. johndoe@mail.com')
                if result in messages:
                    conn.rollback()
                    return make_response(jsonify({"status": "failed", "message": result}), 409)
                if checks is not None:
                    conn.rollback()
                    return jsonify({"status": "failed",
                                    "message": "The email has already been registered, use another"}), 409

                hashed_pwd = generate_password_hash(password, method='sha256')
                cur.execute("INSERT INTO Users(username, email, password) VALUES (%s, %s, %s)",
                            (username, email, hashed_pwd))
                conn.commit()
        return make_response(jsonify({"status": "success", "message": "User has been registered, you can login"}), 201)
