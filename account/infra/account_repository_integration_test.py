from decimal import Decimal
import uuid
import pytest
from testcontainers.postgres import PostgresContainer

from account.domain.account import Account
from account.infra.account_repository import AccountRepository


@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:15") as container:
        yield container


@pytest.fixture
def account_repository(postgres_container):
    dsn = postgres_container.get_connection_url()
    # Remove the '+psycopg2' from the URL if present
    dsn = dsn.replace("postgresql+psycopg2://", "postgresql://")

    repo = AccountRepository(dsn)
    
    # create table
    with repo.get_connection() as conn:
        conn.execute("""
            CREATE TABLE accounts (
                account_id UUID PRIMARY KEY,
                currency VARCHAR NOT NULL,
                balance NUMERIC NOT NULL,
                is_active BOOLEAN NOT NULL
            );
        """)
        conn.commit()
    
    return repo


def test_save_and_get(account_repository):
    account_id = uuid.uuid4()
    account = Account(account_id=account_id, currency="USD", balance=Decimal(1000.0), is_active=True)
    account_repository.save(account)

    fetched = account_repository.get_by_id(account_id)
    
    assert fetched is not None
    assert fetched.account_id == account_id
    assert fetched.currency == "USD"
    assert fetched.balance == 1000.0
    assert fetched.is_active is True
