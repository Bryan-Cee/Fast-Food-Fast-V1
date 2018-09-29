"""__init__"""
from flask import Flask
import os

from app.api.V2.database import InitDB
from instance.config import app_configs


def create_app():
    """Starts the application"""
   
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[os.getenv('APP_SETTINGS')])
    InitDB(app.config).create_tables()
    from app.api.V1.views import V1
    app.register_blueprint(V1)
    return app
