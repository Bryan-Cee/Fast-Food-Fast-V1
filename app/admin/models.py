from flask import jsonify, make_response
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from instance.config import app_configs
import os

from ..users.models import conn as connection


admin_conn = app_configs[os.getenv('APP_SETTINGS')]


class Admin:
    def __init__(self):
        self.conn = connection

    def add_to_menu(self, meal_name, meal_desc, meal_price, pic):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT meal_name FROM Menu WHERE meal_name = %s", (meal_name,))
                checks = cur.fetchone()
                if not meal_name or not meal_price:
                    conn.rollback()
                    return jsonify({"status": "failed",
                                    "message": "Please enter the correct details for a meal i.e. "
                                               "'meal_name': 'mealname', "
                                               "'meal_price': 'price', meal_desc': 'meal_description'"})
                if checks is not None:
                    conn.rollback()
                    return make_response(jsonify({"status": "failed", "message": "The meal is already in the menu"}), 409)
                cur.execute("INSERT INTO Menu(meal_name, meal_desc, meal_price, pic) VALUES (%s, %s, %s, %s)",
                            (meal_name, meal_desc, meal_price, pic))
                conn.commit()
                return make_response(jsonify({"status": "success", "message": "Meal has been added to the menu"}), 201)

    def get_the_menu(self):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM Menu")
                menu = cur.fetchall()
                if not menu:
                    return make_response(jsonify({'status': 'success', 'message': 'There are no meals in the menu at the moment'}))
                return jsonify({"menu": menu})

    def all_orders(self):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT Order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order, quantity, pic "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id order by order_id ASC;")
                orders = cur.fetchall()
                if not orders:
                    return make_response(jsonify({'status': 'success', 'message': 'There are no orders currently'}))
                for order in orders:
                    order['total'] = round(
                        order['quantity'] * order['meal_price'], 2)

                return make_response(jsonify({"Orders": orders}))

    def get_user_orders(self, order_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT order_id, user_id, meal_name, meal_desc, meal_price, order_status, time_of_order, pic, quantity "
                    "FROM Orders "
                    "JOIN Menu ON Menu.meal_id = Orders.meal_id WHERE order_id = %s;", (order_id,))
                history = cur.fetchone()
                if not history:
                    return make_response(jsonify({'status': 'failed', 'message': 'There is no order with that ID'}), 404)
                history['total'] = round(
                    history['quantity'] * history['meal_price'], 2)
                return make_response(jsonify({"Order": history}))

    def get_user(self, user_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT user_id, username, email, admin FROM users WHERE user_id = %s", (user_id,))
                user = cur.fetchone()
                if not user:
                    return make_response(jsonify({'status': 'failed', 'message': "The user doesn't exist"}), 404)
                return make_response(jsonify({
                    "user": user
                }))

    def modify_order(self, order_id, status):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM orders WHERE order_id= %s", (order_id,))
                rows = cur.fetchone()
                if not rows:
                    conn.rollback()
                    return make_response(jsonify({'status': 'failed', 'message': 'There is no such order'}), 404)
                cur.execute(
                    "UPDATE orders SET order_status = %s WHERE order_id = %s", (status, order_id))
                conn.commit()
                return make_response(jsonify({"status": "success", "message": "The order status has been updated"}), 201)

    def promote_user(self, admin, user_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM users WHERE user_id= %s", (user_id,))
                rows = cur.fetchone()
                if not rows:
                    conn.rollback()
                    return jsonify({'status': 'failed', 'message': 'The user does not exist'}), 404
                if not admin or admin not in ('True', 'False'):
                    return jsonify({"status": 'failed', 'message': 'To promote a user or demote a user set '
                                                                   ': "admin": "True" or "admin": "False"'}), 400
                cur.execute(
                    "UPDATE users SET admin = %s WHERE user_id = %s", (admin, user_id))
                conn.commit()
                return jsonify({"status": "success", "message": "The user admin rights have been updated"}), 201

    def del_meal(self, meal_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                try:
                    cur.execute(
                        "DELETE FROM menu WHERE meal_id = %s", (meal_id,))
                except (psycopg2.IntegrityError):
                    conn.rollback()
                    return jsonify({
                        "status": "failed",
                        "message": "This meal is referenced in the orders table it cannot be deleted"
                    })
                finally:
                    conn.commit()

                return jsonify({"status": "success", "message": "Meal has been deleted"})
