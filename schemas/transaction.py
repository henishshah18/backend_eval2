#creating schemas for transaction model
'''
Sample endpoints for transactions:
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



from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import descriptor_props

class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class Transaction(BaseModel):
    id: int
    transaction_type: TransactionType
    amount: float
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionDetail(Transaction):
    user_id: int
    recipient_user_id: Optional[int]
    reference_transaction_id: Optional[int]

    class Config:
        orm_mode = True