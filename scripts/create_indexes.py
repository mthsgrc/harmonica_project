from app import create_app, db
from sqlalchemy import text

app = create_app()

def create_search_indexes():
    with app.app_context():
        with db.engine.connect() as connection:
            # Create indexes for search columns
            connection.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_artist ON tabs (artist COLLATE NOCASE);"
            ))
            connection.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_song ON tabs (song COLLATE NOCASE);"
            ))
            connection.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_genre ON tabs (genre COLLATE NOCASE);"
            ))
            print("Search indexes created successfully")

if __name__ == '__main__':
    create_search_indexes()