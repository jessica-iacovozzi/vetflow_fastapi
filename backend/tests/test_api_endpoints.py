from app.core.config import get_settings

settings = get_settings()

def test_create_policy_endpoint(client):
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

def test_check_consent_status_endpoint(client, test_user):
    response = client.get(f"{settings.API_V1_STR}/user-consents/{test_user.id}/consent-status")
    
    assert response.status_code == 200
    assert "needs_consent" in response.json()

def test_register_user_endpoint(client):
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

def test_access_token_endpoint(client):
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
    assert "user_id" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_get_all_users_endpoint(client, logged_user):
    access_token, _ = logged_user
    response = client.get(f"{settings.API_V1_STR}/users/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_current_user_endpoint(client, logged_user, test_user):
    access_token, _ = logged_user
    response = client.get(f"{settings.API_V1_STR}/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email


""" def test_create_pet_endpoint(client, logged_user):
    access_token, _ = logged_user
    response = client.post(
        f"{settings.API_V1_STR}/pets/",
        json={
            "name": "Test Pet",
            "species": "cat",
            "breed": "Siamese",
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Pet" """


def test_get_all_pets_endpoint(client, logged_user):
    access_token, _ = logged_user
    response = client.get(f"{settings.API_V1_STR}/pets/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_pet_by_id_endpoint(client, logged_user, test_pet):
    access_token, _ = logged_user
    response = client.get(f"{settings.API_V1_STR}/pets/{test_pet.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Pet"


def test_update_pet_endpoint(client, logged_user, test_pet):
    access_token, _ = logged_user
    response = client.put(
        f"{settings.API_V1_STR}/pets/{test_pet.id}",
        json={
            "name": "Updated Pet Name",
            "owner_id": test_pet.owner_id,
            "species": "cat",
            "breed": "Siamese",
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Pet Name"


def test_delete_pet_endpoint(client, logged_user, test_pet):
    access_token, _ = logged_user
    response = client.delete(f"{settings.API_V1_STR}/pets/{test_pet.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204
