"""__init__"""
from flask import Flask, jsonify


def create_app():
    """Starts the application"""
    from app.models import OrderFood

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    orders = OrderFood().get_all_orders()

    @app.route('/api/V1/orders/<int:orderid>', methods=['GET'])
    def get_specific_order(orderid):
        ids = [order for order in orders if order["order_id"] == orderid]
        if not ids:
            return "The order was not found", 404

        return jsonify({"Order": ids})

    return app
