#creating wallet endpoints

'''
Wallet endpoints:
GET /wallet/{user_id}/balance
Response: 200 OK
{
  "user_id": 1,
  "balance": 150.50,
  "last_updated": "2024-01-01T12:30:00Z"
}

POST /wallet/{user_id}/add-money
Request Body:
{
  "amount": 100.00,
  "description": "Added money to wallet"
}
Response: 201 Created
{
  "transaction_id": 123,
  "user_id": 1,
  "amount": 100.00,
  "new_balance": 250.50,
  "transaction_type": "CREDIT"
}

POST /wallet/{user_id}/withdraw
Request Body:
{
  "amount": 50.00,
  "description": "Withdrew money from wallet"
}
Response: 201 Created / 400 Bad Request (insufficient balance)

'''

from crud.crud_wallet import balance_inquiry, add_money, withdraw_money
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.wallet import WalletBalance, WalletAddMoney, WalletAddMoneyResponse, WalletWithdrawMoney

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)

@router.get("/{user_id}/balance", response_model=WalletBalance)
def get_wallet_balance(user_id: int, db: Session = Depends(get_db)):
    balance = balance_inquiry(db, user_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance

@router.post("/{user_id}/add-money", response_model=WalletAddMoneyResponse, status_code=status.HTTP_201_CREATED)
def add_money_to_wallet(user_id: int, money: WalletAddMoney, db: Session = Depends(get_db)):
    response = add_money(db, user_id, money)
    if not response:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return response

@router.post("/{user_id}/withdraw", response_model=WalletAddMoneyResponse, status_code=status.HTTP_201_CREATED)
def withdraw_money_from_wallet(user_id: int, money: WalletWithdrawMoney, db: Session = Depends(get_db)):
    response = withdraw_money(db, user_id, money)
    if response == "Insufficient balance":
        raise HTTPException(status_code=400, detail="Insufficient balance")
    if not response:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return response