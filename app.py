from flask import Flask, send_from_directory
from datetime import timedelta
import os


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.getenv('SECRET_KEY')
    
    # Configure app
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    from blueprints.typing import typing_bp
    app.register_blueprint(typing_bp, url_prefix='/typing')

    return app