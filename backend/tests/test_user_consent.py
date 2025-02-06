from datetime import datetime
from app.crud.policy import create_policy
from app.crud.user_consent import create_user_consent, check_user_consent_status
from app.schemas.user_consent import UserConsentCreate
from app.schemas.policy import PolicyCreate
from app.models.policy import Policy

def test_create_policy(db_session):
    policy_data = PolicyCreate(
        version="v1.0",
        text="Test privacy policy",
        data_purpose="Testing purposes",
        is_active=True
    )
    
    policy = create_policy(db_session, policy_data)
    
    assert policy.version == "v1.0"
    assert policy.text == "Test privacy policy"
    assert policy.is_active == True

def test_create_multiple_active_policies(db_session):
    first_policy = db_session.query(Policy).first()
    
    policy2 = PolicyCreate(
        version="v2.0",
        text="Second policy",
        data_purpose="Testing",
        is_active=True
    )
    second_policy = create_policy(db_session, policy2)
    
    db_session.refresh(first_policy)
    
    assert first_policy.is_active == False
    assert second_policy.is_active == True

def test_create_user_consent(db_session, test_user):
    policy = db_session.query(Policy).first()
    
    consent = create_user_consent(
        db_session,
        UserConsentCreate(
            user_id=test_user.id,
            policy_id=policy.id
        )
    )
    
    assert consent.user_id == test_user.id
    assert consent.policy_id == policy.id
    assert isinstance(consent.consent_date, datetime)

def test_check_user_consent_status(db_session, test_user):
    policy = db_session.query(Policy).filter(Policy.version == "v1.0").first()
    create_user_consent(db_session, UserConsentCreate(user_id=test_user.id, policy_id=policy.id))
    
    status = check_user_consent_status(db_session, test_user.id)
    assert status["needs_consent"] == True
    assert status["reason"] == "New policy requires consent"
    assert status["current_policy_version"] == "v1.0"
    assert status["new_policy_version"] == "v2.0"