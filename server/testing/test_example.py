from models import User

def test_signup(client, db_session):
    # Test data with valid password
    test_data = {
        'username': 'testuser',
        'password': 'ValidPass1',
        'image_url': 'test.jpg',
        'bio': 'Test bio'
    }
    
    response = client.post('/signup', json=test_data)
    
    # Debug output
    print(f"Response Status: {response.status_code}")
    if response.status_code != 201:
        print(f"Response JSON: {response.json}")
    
    assert response.status_code == 201
    assert 'username' in response.json
    assert response.json['username'] == 'testuser'
    
    
    user = db_session.query(User).filter_by(username='testuser').first()
    assert user is not None
    assert user.verify_password('ValidPass1') is True