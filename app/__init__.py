"""__init__"""
from flask import Flask


def create_app():
    """Starts the application"""
    from app.models import OrderFood

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    new_order = OrderFood().get_all_orders()
    menu = OrderFood().current_menu()

    @app.route('/api/V1/orders', methods=['GET', 'POST'])
    def get_all_orders():
        if request.method == 'POST':
            if not new_order:
                order_details = {'order_id': 1,
                                 'foodname': request.json['foodname'],
                                 'status': 'new order'}
            else:
                order_details = {'order_id': new_order[-1]['order_id'] + 1,
                                 'foodname': request.json['foodname'],
                                 'status': 'new order'}

            foodname = [food for food in menu if order_details['foodname'] == food['foodname']]
            if not foodname:
                return "Invalid order, the food you ordered is not in the menu", 400
            new_order.append(order_details)
            return 'Order for {} has been received'.format(order_details['foodname']), 201

        if not new_order:
            return 'No orders yet'

        return jsonify({'Orders': new_order})

    orders = OrderFood().get_all_orders()


    @app.route('/api/V1/orders/<int:orderid>', methods=['GET', 'PUT'])
    def get_specific_order(orderid):
        ids = [order for order in orders if order["order_id"] == orderid]
        if not ids:
            return "The order was not found", 404

        if request.method == 'PUT':
            ids[0]["status"] = request.json["status"]
            return 'Order id {} has been updated'.format(ids[0]["order_id"])

        return jsonify({"Order": ids})

    menu = OrderFood().current_menu()

    @app.route("/api/V1/menu", methods=['POST', 'GET'])
    def add_meal_to_menu():
        if request.method == 'POST':
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

        if not menu:
            return 'No meals have been added to the menu'
        return jsonify(menu)

    return app
