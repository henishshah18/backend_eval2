#Transaction CRUD operations

'''
Transaction related operations:
Transaction Management
Create Transaction: Record debit/credit transactions for users
Transaction History: Retrieve user's transaction history with pagination
Transaction Details: Get specific transaction information
Transaction Types: Support DEBIT, CREDIT, TRANSFER_IN, TRANSFER_OUT

Transaction endpoints:
GET /transactions/{user_id}?page=1&limit=10
Response: 200 OK
{
  "transactions": [
    {
      "transaction_id": 123,
      "transaction_type": "CREDIT",
      "amount": 100.00,
      "description": "Added money",
      "created_at": "2024-01-01T12:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}


GET /transactions/detail/{transaction_id}
Response: 200 OK
{
  "transaction_id": 123,
  "user_id": 1,
  "transaction_type": "TRANSFER_OUT",
  "amount": 25.00,
  "description": "Transfer to jane_doe",
  "recipient_user_id": 2,
  "reference_transaction_id": 124,
  "created_at": "2024-01-01T12:30:00Z"
}

'''

from sqlalchemy.orm import Session
from models.transaction import Transaction
from schemas.transaction import Transaction, TransactionDetail

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit).all()

def get_transactions_detail(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()