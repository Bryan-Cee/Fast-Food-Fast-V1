import os
import psycopg2
import psycopg2.extras
from flask import make_response, jsonify
from instance.config import app_configs

config = app_configs[os.getenv('APP_SETTINGS')]

conn = psycopg2.connect(host="localhost",
                        database=config.DBNAME,
                        user=config.USER,
                        password=config.PASSWORD)


def place_order(meal_id, user_id, time, quantity):
    with conn:
        with conn.cursor() as cur:
            if not meal_id:
                conn.rollback()
                return 'Please enter the correct JSON format: "meal_id":id, "quantity":number"', 400
            try:
                cur.execute("INSERT INTO Orders(meal_id, user_id, time_of_order, quantity) VALUES (%s, %s, %s, %s)",
                            (meal_id, user_id, time, quantity))
            except (Exception, psycopg2.IntegrityError):
                conn.rollback()
                return "The meal does not exists in the menu", 404
            finally:
                conn.commit()
    return "Order has been received", 201


def get_history(user_id):
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT Order_id, meal_name, meal_desc, meal_price,"
                        " order_status, time_of_order, quantity FROM Orders "
                        "JOIN Menu ON Menu.meal_id = Orders.meal_id WHERE Orders.user_id = %s order by time_of_order;",
                        (user_id,))
            history = cur.fetchall()
            for order in history:
                order['total'] = order['quantity'] * order['meal_price']
            if not history:
                return make_response(jsonify({'status': 'You have no history'}))
            return make_response(jsonify({"User_History": history}))
