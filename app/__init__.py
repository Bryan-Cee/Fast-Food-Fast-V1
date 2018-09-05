"""__init__"""
from flask import Flask, jsonify, abort


def create_app():
    """Starts the application"""
    from app.models import ORDERS

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    @app.route('/api/V1/orders/<int:orderid>', methods=['GET'])
    def get_specific_order(orderid):
        ids = [order for order in ORDERS if order["order_id"] == orderid]
        if not ids:
            abort(404)

        return jsonify({"Order": ids})

    return app
