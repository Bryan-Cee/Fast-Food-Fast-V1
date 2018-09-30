import os
import psycopg2
from flask import make_response, jsonify
import ast
import jsonplus as json
from instance.config import app_configs

config = app_configs[os.getenv('APP_SETTINGS')]


conn = psycopg2.connect(host="localhost",
                        database=config.DBNAME,
                        user=config.USER,
                        password=config.PASSWORD)


def place_order(meal_id, user_id, time):
    with conn:
        with conn.cursor() as cur:
            if not meal_id or not user_id:
                conn.rollback()
                return 'Please enter the correct format of keys'
            try:
                cur.execute("INSERT INTO Orders(meal_id, user_id, time_of_order) VALUES (%s, %s, %s)",
                            (meal_id, user_id, time))
            except psycopg2.IntegrityError:
                return "The meal does not exists in the menu"
            finally:
                conn.commit()
    return "Order has been received"


def get_history(user_id):
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT Order_id, meal_name, meal_desc, meal_price, order_status, time_of_order FROM Orders "
                        "JOIN Menu ON Menu.meal_id = Orders.meal_id WHERE Orders.user_id = %s order by time_of_order;",
                        (user_id,))
            history = cur.fetchall()
            if not history:
                return make_response(jsonify({'status': 'You have no history'}))
            user_history = []

            for meal_order in history:
                meal = json.dumps({'order_id': meal_order[0],
                                   'meal_name': meal_order[1],
                                   'meal_desc': meal_order[2],
                                   'meal_price': meal_order[3],
                                   'order_status': meal_order[4],
                                   'time_of_order': meal_order[5]})
                meal = ast.literal_eval(meal)
                meal['time_of_order'] = meal['time_of_order']['__value__']
                user_history.append(meal)

            return make_response(jsonify({"User_History": user_history}))
