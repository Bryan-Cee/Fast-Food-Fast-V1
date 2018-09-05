"""__init__"""
from flask import Flask, jsonify


def create_app():
    """Starts the application"""
    from app.models import ORDERS, MENU

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    @app.route('/api/V1/orders', methods=['GET'])
    def get_all_orders():
        return jsonify({'Orders': ORDERS})

    return app
