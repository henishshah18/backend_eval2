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

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .transfer import Transfer

from database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    transaction_type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    reference_transfer_id: Mapped[int] = mapped_column(ForeignKey("transfers.id"), nullable=True)
    recipient_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="transactions", foreign_keys=[user_id])
    reference_transfer: Mapped["Transfer"] = relationship("Transfer", back_populates="transactions", foreign_keys=[reference_transfer_id])