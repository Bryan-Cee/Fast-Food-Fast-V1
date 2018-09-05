"""__init__"""
from flask import Flask


def create_app():
    """Starts the application"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    return app
