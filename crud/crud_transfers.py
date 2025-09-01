#Transfers CRUD operations
'''
Transfer related operations:

Peer-to-Peer Transfer: Transfer money from one user to another
Transfer Validation: Ensure sender has sufficient balance
Atomic Transactions: Ensure transfer operations are atomic (both debit and credit succeed or fail together)


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

from sqlalchemy.orm import Session
from models.user import User
from models.transaction import Transaction
from models.transfer import Transfer
from schemas.transfer import Transfer, TransferResponse, TransferDetailResponse, TransferErrorResponse


def create_transfer(db: Session, transfer: Transfer):
    sender = db.query(User).filter(User.id == transfer.sender_user_id).first()
    recipient = db.query(User).filter(User.id == transfer.recipient_user_id).first()

    if not sender or not recipient:
        return None, "Sender or recipient not found"

    if sender.wallet.balance < transfer.amount:
        return TransferErrorResponse(
            error="Insufficient balance",
            current_balance=sender.wallet.balance,
            required_amount=transfer.amount
        ), None

    # Deduct amount from sender's wallet
    sender.wallet.balance -= transfer.amount
    # Add amount to recipient's wallet
    recipient.wallet.balance += transfer.amount

    # Create transfer record
    new_transfer = Transfer(
        sender_user_id=transfer.sender_user_id,
        recipient_user_id=transfer.recipient_user_id,
        amount=transfer.amount,
        status="COMPLETED"
    ) 

    db.add(new_transfer)
    db.commit()
    db.refresh(new_transfer)


    # Create transaction records for both users
    sender_transaction = Transaction(
        user_id=transfer.sender_user_id,
        transaction_type="TRANSFER_OUT",
        amount=transfer.amount,
        description=f"Transfer to user {transfer.recipient_user_id}",
        reference_transfer_id=new_transfer.id,
        recipient_user_id=transfer.recipient_user_id
    )
    recipient_transaction = Transaction(
        user_id=transfer.recipient_user_id,
        transaction_type="TRANSFER_IN",
        amount=transfer.amount,
        description=f"Transfer from user {transfer.sender_user_id}",
        reference_transfer_id=new_transfer.id,
        recipient_user_id=transfer.sender_user_id
    )
    db.add(sender_transaction)
    db.add(recipient_transaction)
    db.commit()
    db.refresh(sender_transaction)
    db.refresh(recipient_transaction)

    return TransferResponse(
        transfer_id=new_transfer.id,
        sender_transaction_id=sender_transaction.id,
        recipient_transaction_id=recipient_transaction.id,
        amount=new_transfer.amount,
        sender_new_balance=sender.wallet.balance,
        recipient_new_balance=recipient.wallet.balance,
        status=new_transfer.status
    ), None

def get_transfer(db: Session, transfer_id: int):
    transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not transfer:
        return None
    return TransferDetailResponse(
        transfer_id=transfer.id,
        sender_user_id=transfer.sender_user_id,
        recipient_user_id=transfer.recipient_user_id,
        amount=transfer.amount,
        description=None,
        status=transfer.status,
        created_at=transfer.created_at
    )

