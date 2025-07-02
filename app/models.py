from app import db

class Tab(db.Model):
    __tablename__ = 'tabs'  # Match the actual table name in database
    
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120), nullable=False)
    song = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    harp_type = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    youtube_link = db.Column(db.String(200))

    def __repr__(self):
        return f'<Tab {self.artist} - {self.song}>'