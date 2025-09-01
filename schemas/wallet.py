#creating schemas for wallet model

'''
Wallet model-
id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
wallet_address: Mapped[str] = mapped_column(String, unique=True, index=True)
wallet_type: Mapped[str] = mapped_column(String)
balance: Mapped[float] = mapped_column(default=0.00)
created_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP")
updated_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

'''


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from models import transaction, user

class WalletBase(BaseModel):
    balance: Optional[float] = 0.00

class WalletCreate(WalletBase):
    user_id: int
    wallet_address: str
    balance: Optional[float] = 0.00
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class WalletAddMoney(BaseModel):
    amount: float
    description: Optional[str] = None

class WalletAddMoneyResponse(WalletBase):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str

class WalletWithdrawMoney(BaseModel):
    amount: float
    description: Optional[str] = None

class WalletBalance(WalletBase):
    user_id: int
    updated_at: Optional[datetime] = None