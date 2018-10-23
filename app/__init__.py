"""__init__"""
import os
from flask import Flask, redirect, render_template
from flask_cors import CORS
from app.database import InitDB
from instance.config import app_configs


def create_app():
    """Starts the application"""
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resource={r"/*": {"origins": "*"}})

    app.config.from_object(app_configs[os.getenv('APP_SETTINGS')])

    InitDB().create_tables()

    @app.route('/', methods=['GET'])
    def home():
        return redirect('https://ceebryan.docs.apiary.io/#'), 301

    from app.admin.views import admin_bp
    app.register_blueprint(admin_bp)

    from app.auth.views import auth_bp
    app.register_blueprint(auth_bp)

    from app.users.views import user
    app.register_blueprint(user)

    return app
