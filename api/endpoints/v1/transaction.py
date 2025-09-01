#creating Transaction endpoints

'''
Transaction Endpoints:
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

from crud.crud_transactions import get_transactions, get_transactions_detail
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.transaction import Transaction, TransactionDetail
from typing import List, Optional

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=List[Transaction])
def get_transactions(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    transactions, total = get_transactions(db, user_id=user_id, skip=skip, limit=limit)
    if transactions is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "transactions": transactions,
        "total": total,
        "page": page,
        "limit": limit
    }   

@router.get("/detail/{transaction_id}", response_model=TransactionDetail)
def get_transaction_detail(transaction_id: int, db: Session = Depends(get_db)):
    transaction = get_transactions_detail(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

