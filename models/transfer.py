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

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from .user import User
from .transaction import Transaction

class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column()
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP")
    updated_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    sender: Mapped["User"] = relationship(foreign_keys=[sender_user_id], back_populates="sent_transfers")
    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_user_id], back_populates="received_transfers")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="reference_transfer")