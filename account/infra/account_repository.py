import psycopg
from psycopg.rows import dict_row

from account.domain.account import Account
from account.domain.account_repository import AccountRepositoryInterface

class AccountRepository(AccountRepositoryInterface):
    def __init__(self, dsn: str):
        self.dsn = dsn
    
    def get_connection(self):
        return psycopg.connect(self.dsn, row_factory=dict_row)
    
    def save(self, account: Account):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO accounts (account_id, currency, balance, is_active)
                    VALUES (%s , %s, %s, %s)
                    """,
                    (account.account_id, account.currency, account.balance, account.is_active)
                )
    
    def get_by_id(self, account_id) -> Account | None:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM accounts WHERE account_id = %s",
                    (account_id,)
                )
                row = cursor.fetchone()
                if row:
                    return Account(
                        account_id= row["account_id"],
                        currency = row["currency"],
                        balance = row["balance"],
                        is_active= row["is_active"]

                    )
                else:
                    return None

    
