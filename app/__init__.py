"""__init__"""
from flask import Flask, jsonify, request


def create_app():
    """Starts the application"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    from app.models import OrderFood

    menu = OrderFood().current_menu()

    @app.route("/api/V1/menu", methods=['POST'])
    def add_meal_to_menu():
        mealname = [meal[key] for meal in menu for key in meal.keys() if key == 'foodname']
        if request.json['foodname'] not in mealname:
            if not menu:
                meal = {'order_id': 1,
                        "foodname": request.json['foodname'],
                        "price": request.json['price']}
            else:
                meal = {'order_id': menu[-1]['order_id'] + 1,
                        "foodname": request.json['foodname'],
                        "price": request.json['price']}

            menu.append(meal)

            return 'Meal added', 201

        return 'Meal is already in the menu', 400

    return app
