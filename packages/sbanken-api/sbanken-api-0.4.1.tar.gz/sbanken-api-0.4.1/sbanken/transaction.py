from .auth import Auth
from .const import BANK_SCOPE


class Transaction:
    """ Class that represents a transaction in Sbanken """

    def __init__(self, raw_data: dict, auth: Auth):
        if "item" in raw_data:
            self.raw_data = raw_data["item"]
        else:
            self.raw_data = raw_data
        self.auth = auth

    @property
    def accounting_date(self) -> str:
        return self.raw_data["accountingDate"]

    @property
    def interest_date(self) -> str:
        return self.raw_data["interestDate"]

    @property
    def amount(self) -> float:
        return self.raw_data["amount"]

    @property
    def text(self) -> str:
        return self.raw_data["text"]

    @property
    def transaction_type(self) -> str:
        return self.raw_data["transactionType"]

    @property
    def transaction_code(self) -> int:
        return self.raw_data["transactionCode"]
