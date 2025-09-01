#creating transfer endpoints

'''
Transfer Endpoints:
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

from crud.crud_transfers import create_transfer, get_transfer
from fastapi import APIRouter, Depends, HTTPException, status  
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.transfer import Transfer, TransferResponse, TransferDetailResponse, TransferErrorResponse

router = APIRouter(
    prefix="/transfer",
    tags=["transfer"],
    responses={404: {"description": "Not found"}},
)  

@router.post("/", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def post_transfer(transfer: Transfer, db: Session = Depends(get_db)):
    result, error = create_transfer(db, transfer)
    if error:
        if isinstance(error, TransferErrorResponse):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.dict())
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    return result

@router.get("/{transfer_id}", response_model=TransferDetailResponse)
def get_transfer_detail(transfer_id: str, db: Session = Depends(get_db)):
    transfer = get_transfer(db, transfer_id)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found")
    return transfer