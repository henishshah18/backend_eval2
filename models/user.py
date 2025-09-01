#creating user model

'''
Sample User CREATE statement:
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

from __future__ import annotations

from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from datetime import datetime

if TYPE_CHECKING:
    from .wallet import Wallet
    from .transaction import Transaction
    from .transfer import Transfer

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), server_default="0.00")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    wallets: Mapped[List["Wallet"]] = relationship("Wallet", back_populates="owner")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="user", foreign_keys="Transaction.user_id"
    )
    sent_transfers: Mapped[List["Transfer"]] = relationship(
        "Transfer", back_populates="sender", foreign_keys="Transfer.sender_user_id"
    )
    received_transfers: Mapped[List["Transfer"]] = relationship(
        "Transfer", back_populates="recipient", foreign_keys="Transfer.recipient_user_id"
    )
