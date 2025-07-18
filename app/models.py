# app/models.py
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='viewer')
    favorites = db.relationship(
        'Tab', 
        secondary='favorites', 
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Tab(db.Model):
    __tablename__ = 'tabs'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    song = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String)
    genre = db.Column(db.String)
    harp_type = db.Column(db.String, nullable=False)
    harp_key = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    youtube_link = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='tab', lazy='dynamic')

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tab_id = db.Column(db.Integer, db.ForeignKey('tabs.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))