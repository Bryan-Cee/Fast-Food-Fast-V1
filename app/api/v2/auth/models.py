import os

import psycopg2
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
from instance.config import app_configs
from .validator import credentials_checker

env = os.getenv('APP_SETTINGS')
config = app_configs[env]


class Auth:

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     database=config.DBNAME,
                                     user=config.USER,
                                     password=config.PASSWORD)

    def create_user(self, username, password):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM Users WHERE username = %s", (username,))
                checks = cur.fetchone()
                if not username or not password:
                    conn.rollback()
                    prompt = ('Invalid entry: please enter the correct JSON format - '
                              '"username":"your_username", '
                              '"password":"your_password"')
                    return make_response(prompt)
                if checks is not None:
                    conn.rollback()
                    return 'The username has already been taken please try another', 409
                result = credentials_checker(username, password)
                messages = ('Enter only alphabetic characters for your username',
                            'Enter a password longer than 6 characters',
                            'Password must have atleast one lowercase one upper case and one digit')
                if result in messages:
                    conn.rollback()
                    return make_response(result, 409)
                hashed_pwd = generate_password_hash(password, method='sha256')
                cur.execute("INSERT INTO Users(username, password) VALUES (%s, %s)",
                            (username, hashed_pwd))
                conn.commit()
        return make_response(jsonify({"status": "Success", "message": "User has been registered you can login"}), 201)
