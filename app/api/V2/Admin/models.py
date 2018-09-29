from flask import jsonify, make_response
import psycopg2
from instance.config import app_configs
import os

env = app_configs[os.getenv('APP_SETTINGS')]


class Admin:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     database=env.DBNAME,
                                     user=env.USER,
                                     password=env.PASSWORD)

    def add_to_menu(self, meal_name, meal_desc, meal_price):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT meal_name FROM Menu WHERE meal_name = %s", (meal_name,))
                checks = cur.fetchone()
                if not meal_name or not meal_price:
                    conn.rollback()
                    return 'Please enter the correct format of keys'
                if checks is not None:
                    conn.rollback()
                    return 'The meal is already in the menu'

                cur.execute("INSERT INTO Menu(meal_name, meal_desc, meal_price) VALUES (%s, %s, %s)",
                            (meal_name, meal_desc, meal_price))
                conn.commit()
                return make_response(jsonify({"status": "Meal has been added to the menu"}), 201)

    def get_the_menu(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Menu")
                menu = cur.fetchall()
                if not menu:
                    menu = 'There is no meal in the menu at the moment'
        return jsonify({"menu": menu})
