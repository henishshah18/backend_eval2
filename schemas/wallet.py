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

class WalletBase(BaseModel):
    pass