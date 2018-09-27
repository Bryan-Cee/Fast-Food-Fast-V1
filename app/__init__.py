"""__init__"""
from flask import Flask


def create_app():
    """Starts the application"""
   
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    from .api.V2.database import InitDB
    InitDB.create_tables()

    from app.api.V2.Auth.views import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.V1.views import V1
    app.register_blueprint(V1)

    return app
