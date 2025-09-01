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


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from .wallet import Wallet
from .transaction import Transaction
from .transfer import Transfer
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[float] = mapped_column(default=0.00)
    created_at: Mapped[datetime] = mapped_column(default="CURRENT_TIMESTAMP")
    updated_at: Mapped[datetime] = mapped_column(default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    wallets: Mapped[list["Wallet"]] = relationship(back_populates="owner")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
    sent_transfers: Mapped[list["Transfer"]] = relationship(back_populates="sender", foreign_keys="[Transfer.sender_user_id]")
    received_transfers: Mapped[list["Transfer"]] = relationship(back_populates="recipient", foreign_keys="[Transfer.recipient_user_id]")
