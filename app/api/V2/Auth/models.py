import os

import psycopg2
from flask import make_response, jsonify

from instance.config import app_configs

env = os.getenv('APP_SETTINGS')
config = app_configs[env]


class Auth:

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     database=config.DBNAME,
                                     user=config.USER,
                                     password=config.PASSWORD)

    def create_user(self, username, hashed_pwd, admin):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM Users WHERE username = %s", (username,))
                checks = cur.fetchone()
                if not username or not hashed_pwd:
                    conn.rollback()
                    return 'Invalid, no user name or password'
                if checks is not None:
                    conn.rollback()
                    return 'The username has already been taken please try another'

                cur.execute("INSERT INTO Users(username, password, admin) VALUES (%s, %s, %s)",
                            (username, hashed_pwd, admin))
                conn.commit()
        return make_response(jsonify({"status": "Success", "message": "User has been registered you can login"}), 201)
