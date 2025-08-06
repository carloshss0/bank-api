from enum import Enum

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    BRL = "BRL"
    CAD = "CAD"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_