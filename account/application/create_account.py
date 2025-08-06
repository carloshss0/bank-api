from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from account.application.exceptions import InvalidAccountData
from account.domain.account import Account
from account.domain.account_repository import AccountRepositoryInterface as AccountRepository


@dataclass
class CreateAccountInput:
    currency: str
    balance: Decimal = Decimal(0.0)
    is_active: bool = False

@dataclass
class CreateAccountOutput:
    account_id: UUID

class CreateAccountUseCase:
    def __init__(self, repository: AccountRepository):
        self.repository = repository
    
    def execute(self, input: CreateAccountInput) -> CreateAccountOutput:
        try:
            account = Account(
                currency = input.currency,
                balance= input.balance,
                is_active= input.is_active
            )
        except ValueError as err:
            raise InvalidAccountData(f"Invalid Account data: {err}")
        
        self.repository.save(account)
        return CreateAccountOutput(account_id=account.account_id)