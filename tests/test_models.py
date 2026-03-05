import pytest
from app.models import User, Tab
from werkzeug.security import generate_password_hash

def test_user_creation():
    """Test User model creation and methods"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=generate_password_hash("testpass"),
        role="viewer"
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "viewer"
    assert user.password_hash is not None
    assert str(user) == "testuser"

def test_tab_creation():
    """Test Tab model creation"""
    tab = Tab(
        artist="Bob Dylan",
        song="Blowin' in the Wind",
        difficulty="Intermediate",
        genre="Folk",
        harp_type="Diatonic",
        harp_key="C",
        content="-4 -5 -6 -4\n-5 -6 -5 -4\n",
        youtube_link="https://youtube.com/watch?v=test"
    )
    
    assert tab.artist == "Bob Dylan"
    assert tab.song == "Blowin' in the Wind"
    assert tab.difficulty == "Intermediate"
    assert tab.genre == "Folk"
    assert tab.harp_type == "Diatonic"
    assert tab.harp_key == "C"
    assert "-4 -5 -6" in tab.content
    assert tab.youtube_link == "https://youtube.com/watch?v=test"

def test_tab_validation():
    """Test tab content validation"""
    # Test valid tab
    tab = Tab(
        artist="Test Artist",
        song="Test Song",
        difficulty="Beginner",
        harp_type="Diatonic",
        harp_key="C",
        content="-4 -5 -6"
    )
    assert tab.artist is not None
    assert tab.song is not None
    assert tab.harp_type is not None
    assert tab.harp_key is not None
    assert tab.content is not None

def test_user_favorites_relationship():
    """Test user-favorites relationship"""
    user = User(username="testuser", email="test@example.com", password_hash="hash")
    tab1 = Tab(artist="Artist1", song="Song1", harp_type="Diatonic", harp_key="C", content="test1")
    tab2 = Tab(artist="Artist2", song="Song2", harp_type="Chromatic", harp_key="G", content="test2")
    
    # Test adding favorites
    user.favorites.append(tab1)
    user.favorites.append(tab2)
    
    assert len(user.favorites) == 2
    assert tab1 in user.favorites
    assert tab2 in user.favorites
    assert user in tab1.favorited_by
    assert user in tab2.favorited_by
