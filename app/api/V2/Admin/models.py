from flask import jsonify, make_response
import psycopg2
from instance.config import app_configs
import os
import jsonplus as json
import ast


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

    def all_orders(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT Order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id;")
                history = cur.fetchall()
                if not history:
                    return make_response(jsonify({'status': 'You have no history'}))
                user_history = []

                for meal_order in history:
                    meal = json.dumps({'order_id': meal_order[0],
                                       'user_id': meal_order[1],
                                       'meal_name': meal_order[2],
                                       'meal_desc': meal_order[3],
                                       'meal_price': meal_order[4],
                                       'order_status': meal_order[5],
                                       'time_of_order': meal_order[6]})
                    meal = ast.literal_eval(meal)
                    meal['time_of_order'] = meal['time_of_order']['__value__']
                    user_history.append(meal)

                return make_response(jsonify({"All orders": user_history}))

    def get_user_orders(self, order_id):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT Order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id WHERE order_id = %s;", (order_id,))
                history = cur.fetchall()
                if not history:
                    return make_response(jsonify({'status': 'There is no order with that ID'}))
                order = []

                for meal_order in history:
                    meal = json.dumps({'order_id': meal_order[0],
                                       'user_id': meal_order[1],
                                       'meal_name': meal_order[2],
                                       'meal_desc': meal_order[3],
                                       'meal_price': meal_order[4],
                                       'order_status': meal_order[5],
                                       'time_of_order': meal_order[6]})
                    meal = ast.literal_eval(meal)
                    meal['time_of_order'] = meal['time_of_order']['__value__']
                    order.append(meal)

                return make_response(jsonify({"The order": order}))
