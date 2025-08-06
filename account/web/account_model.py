from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

class AccountCreateRequest(BaseModel):
    account_id: Optional[UUID] = Field(default=None)
    currency: str = Field(min_length=3, max_length=10)
    balance: Optional[Decimal] = Field(default=Decimal(0.0))
    is_active: Optional[bool] = Field(default=False)

class AccountCreateResponse(BaseModel):
    account_id: UUID

class AccountGetResponse(BaseModel):
    account_id: UUID
    currency: str
    balance: Decimal
    is_active: bool