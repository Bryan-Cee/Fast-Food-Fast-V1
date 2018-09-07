"""__init__"""
from flask import Flask, jsonify


def create_app():
    """Starts the application"""
    from app.models import OrderFood

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    @app.route('/api/V1/orders', methods=['GET'])
    def get_all_orders():
        new_order = OrderFood().get_all_orders()
        if not new_order:
            return 'No orders yet'

        return jsonify({'Orders': new_order})

    return app
