# User CRUD operations

'''
User related operations:
User Management
User Profile: Retrieve and update user information
Initial Balance: Users start with a balance of 0.00
Password Security: Passwords are securely hashed


User Profile Endpoints
GET /users/{user_id}
Response: 200 OK
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "balance": 150.50,
  "created_at": "2024-01-01T00:00:00Z"
}

PUT /users/{user_id}
Request Body:
{
  "username": "string",
  "phone_number": "string"
}
Response: 200 OK

'''

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserFetch, UserUpdate
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Helper retrieval functions

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    # Pre-existence checks to avoid IntegrityError
    if get_user_by_email(db, user.email):
        raise ValueError("Email already registered")
    if get_user_by_username(db, user.username):
        raise ValueError("Username already taken")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password,  # store hashed password in password column
        balance=0.00,  # Initial balance
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    data = user_update.dict(exclude_unset=True)
    # Hash password if provided
    if "password" in data and data["password"] is not None:
        data["password"] = get_password_hash(data["password"])
    # Do not allow direct balance manipulation here unless intended
    # (Remove below line if balance updates are allowed)
    # if "balance" in data: del data["balance"]
    for field, value in data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

