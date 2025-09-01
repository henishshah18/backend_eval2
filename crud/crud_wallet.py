#Wallet CRUD operations

'''
Wallet related operations:
Balance Inquiry: Get current wallet balance for a user
Add Money: Credit money to user's wallet (CREDIT transaction)
Withdraw Money: Debit money from user's wallet (DEBIT transaction)
Money Transfer: Transfer money between two users

Wallet Endpoints
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

from fastapi import status
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.orm import Session
from models.wallet import Wallet
from models.user import User
from models.transaction import Transaction
from schemas.wallet import WalletAddMoney, WalletWithdrawMoney, WalletAddMoneyResponse, WalletBase, WalletCreate, WalletBalance
from datetime import datetime


def create_wallet_for_user(db: Session, user_id: int):
    db_wallet = Wallet(
        user_id=user_id,
        wallet_address=f"wallet_{user_id}",
        balance=0.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def balance_inquiry(db: Session, user_id: int):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        return None
    return WalletBalance(
        user_id=wallet.user_id,
        balance=wallet.balance,
        updated_at=wallet.updated_at
    )

def add_money(db: Session, user_id: int, money: WalletAddMoney):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        return None

    # Update wallet balance
    wallet.balance += money.amount
    wallet.updated_at = datetime.utcnow()
    db.add(wallet)

    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        amount=money.amount,
        transaction_type="CREDIT",
        description=money.description,
        created_at=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)
    db.refresh(transaction)

    return WalletAddMoneyResponse(
        transaction_id=transaction.id,
        user_id=user_id,
        amount=money.amount,
        new_balance=wallet.balance,
        transaction_type="CREDIT"
    )

def withdraw_money(db: Session, user_id: int, money: WalletWithdrawMoney):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise ValueError("Wallet not found")
    if wallet.balance < money.amount:
        raise ValueError("Insufficient balance")

    # Update wallet balance
    wallet.balance -= money.amount
    wallet.updated_at = datetime.utcnow()
    db.add(wallet)

    # Create transaction record
    transaction = Transaction(
        user_id=user_id,
        amount=money.amount,
        transaction_type="DEBIT",
        description=money.description,
        created_at=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)
    db.refresh(transaction)

    return status.HTTP_201_CREATED

