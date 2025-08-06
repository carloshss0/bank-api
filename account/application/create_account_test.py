from decimal import Decimal
from uuid import UUID
import pytest
from unittest.mock import MagicMock

from account.application.exceptions import InvalidAccountData
from account.domain.account_repository import AccountRepositoryInterface as AccountRepository
from account.application.create_account import CreateAccountInput, CreateAccountUseCase


class TestCreateAccountUseCase:

    def test_create_account(self):
        mock_repository = MagicMock(AccountRepository)
        use_case = CreateAccountUseCase(repository = mock_repository)

        input = CreateAccountInput(
            currency = "USD",
            balance = Decimal(100.00),
            is_active=True,
        )

        output = use_case.execute(input)

        assert output.account_id is not None
        assert isinstance(output.account_id, UUID)
        assert mock_repository.save.called is True

    def test_create_account_with_invalid_data(self):
        mock_repository = MagicMock(AccountRepository)
        use_case = CreateAccountUseCase(
            repository=mock_repository
        )
        currency = "MEX"
        with pytest.raises(InvalidAccountData, match=f"Unsupported currency: {currency}"):
            use_case.execute(
                CreateAccountInput(
                    currency = currency,  # Invalid currency
                )
            )

