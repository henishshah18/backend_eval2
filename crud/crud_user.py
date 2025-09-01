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

from venv import create
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserFetch, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        balance=0.00,  # Initial balance
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> UserFetch:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for var, value in vars(user_update).items():
        if value is not None:
            setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user

