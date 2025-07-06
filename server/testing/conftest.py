import sys
import os
import pytest

# Add server directory to Python path
server_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, server_dir)

from app import create_app
import extensions as extensions

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    # Push application context
    with app.app_context():
        # Create all tables
        extensions.db.create_all()
        yield app
        extensions.db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Provide a database session for tests."""
    with app.app_context():
        yield extensions.db.session
        extensions.db.session.rollback()