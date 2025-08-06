from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from account.application.exceptions import AccountNotFound
from account.domain.account_repository import AccountRepositoryInterface as AccountRepository


@dataclass
class GetAccountInput:
    account_id: UUID

@dataclass
class GetAccountOutput:
    account_id: UUID
    currency: str
    balance: Decimal
    is_active: bool

class GetAccountUseCase:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def execute(self, input: GetAccountInput) -> GetAccountOutput:
        account = self.repository.get_by_id(input.account_id)
        if not account:
            raise AccountNotFound(f"Account with account_id: {input.account_id} not found.")
        
        return GetAccountOutput(
            account_id= account.account_id,
            currency = account.currency,
            balance= account.balance,
            is_active= account.is_active
        )