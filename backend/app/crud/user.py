from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    print(f"Creating user with password: {repr(user.password)} (length: {len(user.password)})")
    hashed_password = get_password_hash(user.password)
    print(f"Hashed password: {repr(hashed_password)}")
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    print(f"Authenticating user: {email} with password: {repr(password)} (length: {len(password)})")
    user = get_user_by_email(db, email)
    if not user:
        print("User not found")
        return False
    print(f"Found user with hashed password: {repr(user.hashed_password)}")
    if not verify_password(password, user.hashed_password):
        print("Password verification failed")
        return False
    print("Authentication successful")
    return user
