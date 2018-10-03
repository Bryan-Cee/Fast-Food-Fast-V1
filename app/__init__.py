"""__init__"""
import os
from flask import Flask

from app.api.v2.database import InitDB
from instance.config import app_configs


def create_app():
    """Starts the application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[os.getenv('APP_SETTINGS')])

    InitDB(app.config).create_tables()
    from app.api.v2.admin.views import admin_bp
    app.register_blueprint(admin_bp)

    from app.api.v2.auth.views import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.v2.users.views import user
    app.register_blueprint(user)

    from app.api.v1.views import V1
    app.register_blueprint(V1)

    return app
