#creating user endpoints

'''
User endpoints:
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

from crud import crud_user, crud_wallet
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.user import UserCreate, UserFetch, UserUpdate
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=UserFetch)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserFetch)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=UserFetch, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.create_user(db, user=user)
    # Create an associated wallet (side effect) but do not include in response since response_model expects UserFetch
    crud_wallet.create_wallet_for_user(db, user_id=db_user.id)
    return db_user

