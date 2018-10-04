
from flask import jsonify, make_response
import psycopg2
import psycopg2.extras
from instance.config import app_configs
import os


admin_conn = app_configs[os.getenv('APP_SETTINGS')]


class Admin:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost",
                                     database=admin_conn.DBNAME,
                                     user=admin_conn.USER,
                                     password=admin_conn.PASSWORD)

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
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM Menu")
                menu = cur.fetchall()
                if not menu:
                    return make_response(jsonify({'status': 'There are no meals in the menu'}))
                return jsonify({"menu": menu})

    def all_orders(self):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT Order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id;")
                orders = cur.fetchall()
                if not orders:
                    return make_response('There are no orders currently')
                return make_response(jsonify({"All orders": orders}))

    def get_user_orders(self, order_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id WHERE order_id = %s;", (order_id,))
                history = cur.fetchall()
                if not history:
                    return make_response(jsonify({'status': 'There is no order with that ID'}))
                return make_response(jsonify({"The order": history}))

    def modify_order(self, order_id, status):
        with self.conn as conn:
            with conn.cursor() as cur:
                    cur.execute("SELECT * FROM orders WHERE order_id= %s", (order_id,))
                    rows = cur.fetchone()
                    if not rows:
                        conn.rollback()
                        return 'There is no such order'
                    cur.execute("UPDATE orders SET order_status = %s WHERE order_id = %s", (status, order_id))
                    conn.commit()
                    return "The order status has been updated"

    def promote_user(self, admin, user_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE user_id= %s", (user_id,))
                rows = cur.fetchone()
                if not rows:
                    conn.rollback()
                    return 'The user does not exist', 404
                if not admin or admin not in ('True', 'False'):
                    return 'Please enter the correct JSON format: "admin": "True" or "admin": "False"', 400
                cur.execute("UPDATE users SET admin = %s WHERE user_id = %s", (admin, user_id))
                conn.commit()
                return "The user admin rights have been updated", 201
