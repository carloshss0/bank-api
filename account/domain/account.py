from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
import uuid

from account.domain.currency import Currency

@dataclass
class Account:
    currency: str
    balance: Decimal = Decimal(0.0)
    is_active: bool = False
    account_id: UUID = field(default_factory= uuid.uuid4)

    def __post_init__(self): ## Maybe I can refactor this later, it can generate a lot of if/elses in the future...let's see.
        if not isinstance(self.balance, Decimal):
            raise TypeError("Balance must be a Decimal type.")
        if self.balance < Decimal(0):
            raise ValueError("Initial balance cannot be negative.")
        if not isinstance(self.account_id, UUID):
            raise ValueError("Account ID must be a UUID.")
        
        if not Currency.has_value(self.currency):
            raise ValueError(f"Unsupported currency: {self.currency}")

    def activate(self):
        """Activate the account."""
        self.is_active = True

    def deactivate(self):
        """Deactivate the account."""
        self.is_active = False
    
    def deposit(self, amount: Decimal):
        """Deposit an amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: Decimal):
        """Withdraw an amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount

    def get_balance(self) -> Decimal:
        """Return the current balance of the account."""
        return self.balance

    def __str__(self):
        return f"Account({self.account_id}, {self.currency}, Balance: {self.balance}, Active: {self.is_active})"