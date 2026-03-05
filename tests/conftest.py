import pytest
from app import create_app, db
from app.models import User, Tab

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key"
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create CLI test runner"""
    return app.test_cli_runner()

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        role="viewer"
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def sample_tab(app):
    """Create a sample tab for testing"""
    tab = Tab(
        artist="Test Artist",
        song="Test Song",
        difficulty="Beginner",
        genre="Test Genre",
        harp_type="Diatonic",
        harp_key="C",
        content="Test tab content\n-4 -5 -6\n",
        youtube_link="https://youtube.com/watch?v=test"
    )
    db.session.add(tab)
    db.session.commit()
    return tab
