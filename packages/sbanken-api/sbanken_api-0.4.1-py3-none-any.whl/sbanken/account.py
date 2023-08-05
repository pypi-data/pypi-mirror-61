from .auth import Auth
from .const import BANK_SCOPE


class Account:
    """ Class that represents an account in Sbanken """

    def __init__(self, raw_data: dict, auth: Auth):
        if "item" in raw_data:
            self.raw_data = raw_data["item"]
        else:
            self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> str:
        return self.raw_data["accountId"]

    @property
    def account_number(self) -> str:
        return self.raw_data["accountNumber"]

    @property
    def account_type(self) -> str:
        return self.raw_data["accountType"]

    @property
    def name(self) -> str:
        return self.raw_data["name"]

    @property
    def balance(self) -> float:
        return self.raw_data["balance"]

    @property
    def available(self) -> float:
        return self.raw_data["available"]

    @property
    def credit_limit(self) -> float:
        return self.raw_data["creditLimit"]

    async def async_update(self):
        """ Update account data """
        response = await self.auth.request("get", BANK_SCOPE + "/accounts/" + self.id)
        response.raise_for_status()
        self.raw_data = await response.json()
