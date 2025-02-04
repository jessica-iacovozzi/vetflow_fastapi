from app.models.user import User
from app.core.config import get_settings

settings = get_settings()

def test_create_policy_endpoint(client, db_session):
    response = client.post(
        f"{settings.API_V1_STR}/policies/",
        json={
            "version": "v1.0",
            "text": "Test policy",
            "data_purpose": "Testing purposes",
            "is_active": True
        }
    )
    
    assert response.status_code == 200
    assert response.json()["version"] == "v1.0"
    assert response.json()["is_active"] == True

def test_check_consent_status_endpoint(client, db_session):
    user = User(email="test@example.com", hashed_password="test_hash")
    db_session.add(user)
    db_session.commit()
    
    response = client.get(f"{settings.API_V1_STR}/user-consents/{user.id}/consent-status")
    
    assert response.status_code == 200
    assert "needs_consent" in response.json()

def test_register_user_endpoint(client, db_session):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "consent": True
        }
    )
    
    print(response.json())
    assert response.status_code == 200
    
    user = db_session.query(User).filter(User.email == "newuser@example.com").first()
    assert user
    assert user.email == "newuser@example.com"

def test_login_user_endpoint(client, db_session):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "newuser@example.com",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()
    
    user = db_session.query(User).filter(User.email == "newuser@example.com").first()
    assert user
    assert user.email == "newuser@example.com"

