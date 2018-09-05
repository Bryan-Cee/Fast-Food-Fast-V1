"""__init__"""
from flask import Flask, jsonify, request, abort


def create_app():
    """Starts the application"""
    from app.models import ORDERS, MENU

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    new_order = [order for order in ORDERS]

    @app.route('/api/V1/orders', methods=['GET', 'POST'])
    def get_all_orders():
        if request.method == 'POST':
            order_details = {'order_id': new_order[-1]['order_id'] + 1,
                             'foodname': request.json['foodname'],
                             'status': 'new order'}
            foodname = [food for food in MENU if order_details['foodname'] == food['foodname']]
            if not foodname:
                abort(404)

            new_order.append(order_details)
            return 'Order for {} has been received'.format(order_details['foodname']), 201

        return jsonify({'Orders': new_order})

    return app
