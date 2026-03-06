# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config  # Import config dictionary
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_markdown import markdown

csrf = CSRFProtect()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # Use environment-specific config

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app) 

    # Register blueprints
    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    from .admin.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    # Context processor for current year
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}
    
    markdown(app)
    
    return app