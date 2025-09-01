#creating transaction model

'''
Sample Transaction CREATE statement:
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(20) NOT NULL, -- 'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    reference_transaction_id INTEGER REFERENCES transactions(id), -- For linking transfer transactions
    recipient_user_id INTEGER REFERENCES users(id), -- For transfers
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''


from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from .user import User
from .transfer import Transfer

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    transaction_type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column(Text, nullable=True)
    reference_transfer_id: Mapped[int] = mapped_column(ForeignKey("transfers.id"), nullable=True)
    recipient_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP")
    updated_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    user: Mapped["User"] = relationship(back_populates="transactions")
    reference_transfer: Mapped["Transfer"] = relationship(back_populates="transactions")