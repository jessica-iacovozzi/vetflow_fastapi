from app.core.config import get_settings

settings = get_settings()

def test_create_policy_endpoint(client, db_session):
    response = client.post(
        f"{settings.API_V1_STR}/policies/",
        json={
            "version": "v1.0.test",
            "text": "Test policy",
            "data_purpose": "Testing purposes",
            "is_active": True
        }
    )

    assert response.status_code == 200
    assert response.json()["version"] == "v1.0.test"
    assert response.json()["is_active"] is True

def test_check_consent_status_endpoint(client, db_session, test_user):
    response = client.get(f"{settings.API_V1_STR}/user-consents/{test_user.id}/consent-status")
    
    assert response.status_code == 200
    assert "needs_consent" in response.json()

def test_register_user_endpoint(client, db_session):
    test_email = "newuser@example.com"
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": test_email,
            "password": "testpassword",
            "full_name": "Test User",
            "consent_to_policy": True
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == test_email

def test_login_user_endpoint(client, db_session, test_user):
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
