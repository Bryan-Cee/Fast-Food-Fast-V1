"""__init__"""
from flask import Flask, jsonify, abort, request


def create_app():
    """Starts the application"""
    from app.models import ORDERS

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    @app.route('/api/V1/orders/<int:orderid>', methods=['GET', 'PUT'])
    def get_specific_order(orderid):
        ids = [order for order in ORDERS if order["order_id"] == orderid]
        if not ids:
            abort(404)

        if request.method == 'PUT':
            ids[0]["status"] = request.json["status"]
            return 'Order id {} has been updated'.format(ids[0]["order_id"])

        return jsonify({"Order": ids})

    return app
