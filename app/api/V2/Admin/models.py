from flask import jsonify, make_response
import psycopg2
import app.config as config

class Admin:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     database=config.DBNAME,
                                     user=config.USER,
                                     password=config.PASSWORD)

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
                return make_response(jsonify({"status": "Meal has been added to the menu"}))

    def get_the_menu(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Menu")
                menu = cur.fetchall()
        return jsonify({"menu": menu})
