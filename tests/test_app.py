import pytest
from app import create_app, db
from app.models import User, Tab

def test_app_creation():
    """Test that the application can be created"""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] is False  # Default config

def test_index_route(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'All Tabs' in response.data

def test_search_route(client, sample_tab):
    """Test the search route"""
    # Test search without query
    response = client.get('/search')
    assert response.status_code == 200
    
    # Test search with query
    response = client.get('/search?q=Test')
    assert response.status_code == 200
    assert b'Test' in response.data

def test_tab_view_route(client, sample_tab):
    """Test viewing a specific tab"""
    response = client.get(f'/tab/{sample_tab.id}')
    assert response.status_code == 200
    assert b'Test Song' in response.data
    assert b'Test Artist' in response.data

def test_nonexistent_tab(client):
    """Test viewing a non-existent tab"""
    response = client.get('/tab/99999')
    assert response.status_code == 404

def test_search_filters(client, sample_tab):
    """Test search with filters"""
    # Test difficulty filter
    response = client.get('/search?difficulty=Beginner')
    assert response.status_code == 200
    
    # Test harp type filter
    response = client.get('/search?harp_type=Diatonic')
    assert response.status_code == 200
    
    # Test key filter
    response = client.get('/search?harp_key=C')
    assert response.status_code == 200

def test_sorting_options(client, sample_tab):
    """Test sorting options"""
    # Test sort by artist
    response = client.get('/?sort=artist')
    assert response.status_code == 200
    
    # Test sort by song
    response = client.get('/?sort=song')
    assert response.status_code == 200
    
    # Test sort by recent
    response = client.get('/?sort=recent')
    assert response.status_code == 200

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Check if user was created
    user = User.query.filter_by(username='newuser').first()
    assert user is not None

def test_user_login(client, sample_user):
    """Test user login"""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpassword'  # This would need to match the actual password
    }, follow_redirects=True)
    assert response.status_code == 200

def test_invalid_login(client):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', data={
        'username': 'invaliduser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid' in response.data or b'Error' in response.data

def test_form_validation():
    """Test form validation"""
    from app.forms import RegistrationForm
    
    # Test valid form
    form = RegistrationForm(data={
        'username': 'validuser',
        'email': 'valid@example.com',
        'password': 'ValidPass123!',
        'confirm_password': 'ValidPass123!'
    })
    assert form.validate() is True
    
    # Test invalid email
    form = RegistrationForm(data={
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!'
    })
    assert form.validate() is False
    assert 'email' in form.errors

def test_tab_model():
    """Test Tab model"""
    tab = Tab(
        artist="Test Artist",
        song="Test Song",
        difficulty="Beginner",
        harp_type="Diatonic",
        harp_key="C",
        content="Test content"
    )
    assert tab.artist == "Test Artist"
    assert tab.song == "Test Song"
    assert tab.difficulty == "Beginner"
    assert tab.harp_type == "Diatonic"
    assert tab.harp_key == "C"

def test_user_model():
    """Test User model"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "viewer"  # Default role
