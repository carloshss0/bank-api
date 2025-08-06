from abc import ABC, abstractmethod

from account.domain.account import Account

class AccountRepositoryInterface(ABC):
    @abstractmethod
    def save(self, account):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, account_id) -> Account | None:
        raise NotImplementedError
    
