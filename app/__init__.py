# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config  # Import directly from config
from datetime import datetime
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Use the class-based config
    app.config.from_pyfile('../config.py')


    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)  # Add this line


    # Register blueprints
    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Context processor for current year
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}
    
    return app