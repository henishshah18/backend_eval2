#creating Transfer model
'''
Sample Transfer CREATE statement:
CREATE TABLE transfers (
    id SERIAL PRIMARY KEY,
    sender_user_id INTEGER REFERENCES users(id),
    recipient_user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'PENDING', 'COMPLETED', 'FAILED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''' 

from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

from database.db import Base

class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_user_id], back_populates="sent_transfers")
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_user_id], back_populates="received_transfers")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="reference_transfer", foreign_keys="Transaction.reference_transfer_id")