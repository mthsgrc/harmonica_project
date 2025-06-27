from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Import Config directly from config module
try:
    from config import Config
except ImportError:
    # Fallback for different directory structures
    from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    # Context processor for current year
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}
    
    return app