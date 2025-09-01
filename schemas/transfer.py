#creating schemas for transfer model

'''
Transfer endpoints:
POST /transfer
Request Body:
{
  "sender_user_id": 1,
  "recipient_user_id": 2,
  "amount": 25.00,
  "description": "Payment for dinner"
}
Response: 201 Created
{
  "transfer_id": "unique_transfer_id",
  "sender_transaction_id": 123,
  "recipient_transaction_id": 124,
  "amount": 25.00,
  "sender_new_balance": 125.50,
  "recipient_new_balance": 75.00,
  "status": "completed"
}

Response: 400 Bad Request
{
  "error": "Insufficient balance",
  "current_balance": 10.00,
  "required_amount": 25.00
}

GET /transfer/{transfer_id}
Response: 200 OK
{
  "transfer_id": "unique_transfer_id",
  "sender_user_id": 1,
  "recipient_user_id": 2,
  "amount": 25.00,
  "description": "Payment for dinner",
  "status": "completed",
  "created_at": "2024-01-01T12:30:00Z"
}
'''

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TransferStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Transfer(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float

class TransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: TransferStatus

class TransferErrorResponse(BaseModel):
    error: str
    current_balance: float
    required_amount: float

class TransferDetailResponse(BaseModel):
    transfer_id: str
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: Optional[str]
    status: TransferStatus
    created_at: datetime