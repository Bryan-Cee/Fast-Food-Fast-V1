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

    @app.route('/api/V1/orders/<int:orderid>', methods=['GET'])
    def get_specific_order(orderid):
        ids = [order for order in orders if order["order_id"] == orderid]
        if not ids:
            return "The order was not found", 404

        return jsonify({"Order": ids})

    return app
