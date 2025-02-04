from datetime import datetime
from app.crud import user_consent as consent_crud
from app.schemas.user_consent import PolicyCreate
from app.models.user import User

def test_create_policy(db_session):
    policy_data = PolicyCreate(
        version="v1.0",
        text="Test privacy policy",
        data_purpose="Testing purposes",
        is_active=True
    )
    
    policy = consent_crud.create_policy(db_session, policy_data)
    
    assert policy.version == "v1.0"
    assert policy.text == "Test privacy policy"
    assert policy.is_active == True

def test_create_multiple_active_policies(db_session):
    policy1 = PolicyCreate(
        version="v1.0",
        text="First policy",
        data_purpose="Testing",
        is_active=True
    )
    first_policy = consent_crud.create_policy(db_session, policy1)
    
    policy2 = PolicyCreate(
        version="v2.0",
        text="Second policy",
        data_purpose="Testing",
        is_active=True
    )
    second_policy = consent_crud.create_policy(db_session, policy2)
    
    db_session.refresh(first_policy)
    
    assert first_policy.is_active == False
    assert second_policy.is_active == True

def test_create_user_consent(db_session):
    user = User(email="test@example.com", hashed_password="test_hash")
    db_session.add(user)
    db_session.commit()
    
    policy_data = PolicyCreate(
        version="v1.0",
        text="Test policy",
        data_purpose="Testing",
        is_active=True
    )
    policy = consent_crud.create_policy(db_session, policy_data)
    
    consent = consent_crud.create_user_consent(
        db_session,
        user_id=user.id,
        policy_id=policy.id
    )
    
    assert consent.user_id == user.id
    assert consent.policy_id == policy.id
    assert isinstance(consent.consent_date, datetime)

def test_check_user_consent_status(db_session):
    user = User(email="test@example.com", hashed_password="test_hash")
    db_session.add(user)
    db_session.commit()
    
    policy1 = PolicyCreate(
        version="v1.0",
        text="First policy",
        data_purpose="Testing",
        is_active=True
    )
    first_policy = consent_crud.create_policy(db_session, policy1)
    consent_crud.create_user_consent(db_session, user.id, first_policy.id)
    
    status = consent_crud.check_user_consent_status(db_session, user.id)
    assert status["needs_consent"] == False
    
    policy2 = PolicyCreate(
        version="v2.0",
        text="Second policy",
        data_purpose="Testing",
        is_active=True
    )
    consent_crud.create_policy(db_session, policy2)
    
    status = consent_crud.check_user_consent_status(db_session, user.id)
    assert status["needs_consent"] == True
    assert status["reason"] == "New policy requires consent"
    assert status["current_policy_version"] == "v1.0"
    assert status["new_policy_version"] == "v2.0"