#!/usr/bin/env python3
"""
Database migration script for moving from SQLite to PostgreSQL
Run this script after setting up your PostgreSQL database on Render.com
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # SQLite connection
    sqlite_db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'harmonica_tabs.db')
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # PostgreSQL connection (use environment variable)
    postgres_url = os.environ.get('DATABASE_URL')
    if not postgres_url:
        print("ERROR: DATABASE_URL environment variable not set")
        print("Set it to your PostgreSQL connection string")
        return False
    
    try:
        # Parse DATABASE_URL for psycopg2
        import re
        pattern = r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
        match = re.match(pattern, postgres_url)
        
        if not match:
            print("ERROR: Invalid DATABASE_URL format")
            return False
            
        user, password, host, port, dbname = match.groups()
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=user,
            password=password
        )
        pg_cursor = pg_conn.cursor()
        
        print("Connected to both databases successfully")
        
        # Migrate users
        print("Migrating users...")
        sqlite_cursor.execute("SELECT * FROM user")
        users = sqlite_cursor.fetchall()
        
        for user_row in users:
            pg_cursor.execute("""
                INSERT INTO user (id, username, email, password_hash, role, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                user_row['id'],
                user_row['username'],
                user_row['email'],
                user_row['password_hash'],
                user_row['role'],
                user_row['created_at']
            ))
        
        # Migrate tabs
        print("Migrating tabs...")
        sqlite_cursor.execute("SELECT * FROM tabs")
        tabs = sqlite_cursor.fetchall()
        
        for tab_row in tabs:
            pg_cursor.execute("""
                INSERT INTO tabs (id, artist, song, difficulty, genre, harp_type, harp_key, content, youtube_link, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                tab_row['id'],
                tab_row['artist'],
                tab_row['song'],
                tab_row['difficulty'],
                tab_row['genre'],
                tab_row['harp_type'],
                tab_row['harp_key'],
                tab_row['content'],
                tab_row['youtube_link'],
                tab_row['created_at']
            ))
        
        # Migrate favorites
        print("Migrating favorites...")
        sqlite_cursor.execute("SELECT * FROM favorites")
        favorites = sqlite_cursor.fetchall()
        
        for fav_row in favorites:
            pg_cursor.execute("""
                INSERT INTO favorites (id, user_id, tab_id, created_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                fav_row['id'],
                fav_row['user_id'],
                fav_row['tab_id'],
                fav_row['created_at']
            ))
        
        # Commit all changes
        pg_conn.commit()
        print("Migration completed successfully!")
        
        # Print summary
        print(f"Users migrated: {len(users)}")
        print(f"Tabs migrated: {len(tabs)}")
        print(f"Favorites migrated: {len(favorites)}")
        
        return True
        
    except Exception as e:
        print(f"Migration error: {e}")
        return False
    finally:
        sqlite_conn.close()
        if 'pg_conn' in locals():
            pg_conn.close()

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    from app import create_app, db
    from app.models import User
    
    app = create_app()
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin_pass = generate_password_hash('admin123')  # Change this password!
            admin_user = User(
                username='admin',
                email='admin@harmonica-tabs.com',
                password_hash=admin_pass,
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create-admin':
        create_admin_user()
    else:
        migrate_data()
