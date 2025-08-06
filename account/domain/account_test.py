from decimal import Decimal
import uuid
import pytest

from account.domain.account import Account

@pytest.fixture
def create_uuid():
    return uuid.uuid4()

class TestAccount:
    def test_account_creation(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD")
        assert account.account_id == account_id
        assert account.currency == "USD"
        assert account.balance == Decimal(0.0)
        assert not account.is_active

    def test_account_creation_with_invalid_currency(self, create_uuid):
        account_id = create_uuid
        currency = "MEX"
        with pytest.raises(ValueError, match=f"Unsupported currency: {currency}"):
            account = Account(account_id=account_id, currency=currency)

    def test_activate_account(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD")
        account.activate()
        assert account.is_active

    def test_deactivate_account(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD", is_active=True)
        account.deactivate()
        assert not account.is_active

    def test_deposit_funds(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD")
        account.deposit(Decimal("100.00"))
        assert account.balance == Decimal("100.00")

    def test_deposit_negative_funds(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD")
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            account.deposit(Decimal("-50.00"))

    def test_withdraw_funds(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD", balance=Decimal("200.00"))
        account.withdraw(Decimal("50.00"))
        assert account.balance == Decimal("150.00")

    def test_withdraw_with_negative_funds(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD", balance=Decimal("200.00"))
        with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
            account.withdraw(Decimal("-50.00"))

    def test_withdraw_when_exceeding_existing_valance(self, create_uuid):
        account_id = create_uuid
        account = Account(account_id=account_id, currency="USD", balance=Decimal("50.00"))
        with pytest.raises(ValueError, match="Insufficient funds for withdrawal"):
            account.withdraw(Decimal("150.00"))