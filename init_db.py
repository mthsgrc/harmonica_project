# scripts/init_db.py
import os
import sys
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from app.models import User, Tab, Favorite  # Assuming you have these models

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        if not User.query.filter_by(username='123').first():
            admin_pass = generate_password_hash('admin_password')
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=admin_pass,
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_db()