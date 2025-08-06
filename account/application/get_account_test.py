from decimal import Decimal
from uuid import UUID
import uuid
import pytest
from unittest.mock import MagicMock

from account.application.exceptions import AccountNotFound
from account.application.get_account import GetAccountInput, GetAccountUseCase
from account.domain.account import Account
from account.domain.account_repository import AccountRepositoryInterface as AccountRepository

class TestGetAccount:

    def test_get_account_with_existing_account_id(self):
        account = Account(
            currency = "USD",
            balance = Decimal(100.00),
            is_active = True
        )
        mock_repository = MagicMock(AccountRepository)
        mock_repository.get_by_id.return_value = account

        use_case = GetAccountUseCase(repository= mock_repository)

        input = GetAccountInput(
            account_id = account.account_id
        )

        output = use_case.execute(input)

        assert isinstance(output.account_id, UUID)
        assert output.currency == account.currency
        assert output.balance == account.balance
        assert output.is_active == account.is_active
        assert mock_repository.get_by_id.called is True

    def test_get_account_with_non_existing_account_id(self):
        mock_repository = MagicMock(AccountRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetAccountUseCase(repository= mock_repository)

        input = GetAccountInput(account_id= uuid.uuid4())

        with pytest.raises(AccountNotFound, match=f"Account with account_id: {input.account_id} not found."):
            use_case.execute(input)