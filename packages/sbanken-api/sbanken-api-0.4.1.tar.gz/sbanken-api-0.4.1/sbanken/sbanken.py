from typing import List

from .auth import Auth
from .account import Account
from .transaction import Transaction
from .efaktura import Efaktura
from .const import BANK_SCOPE, CUSTOMER_SCOPE


class SbankenAPI:
    """ Class for communication with Sbanken API """

    def __init__(self, auth: Auth):
        """ Initialize API and store Auth """
        self.auth = auth

    async def async_get_accounts(self) -> List[Account]:
        response = await self.auth.request("get", f"{BANK_SCOPE}/accounts/")
        response.raise_for_status()

        j = await response.json()

        return [Account(account_data, self.auth) for account_data in j["items"]]

    async def async_get_account(self, accountId: str) -> Account:
        """ Return the account data """
        response = await self.auth.request("get", f"{BANK_SCOPE}/accounts/{accountId}")
        response.raise_for_status()
        return Account(await response.json(), self.auth)

    async def async_get_transactions(self, accountId: str):
        """ Return transaction data for an account """
        response = await self.auth.request(
            "get", f"{BANK_SCOPE}/transactions/{accountId}"
        )
        response.raise_for_status()

        j = await response.json()
        return [
            Transaction(transaction_data, self.auth) for transaction_data in j["items"]
        ]

    async def async_get_efakturas(self):
        """ Return eFaktura (electronic bill) data for a customer """
        response = await self.auth.request("get", f"{BANK_SCOPE}/efakturas/")
        response.raise_for_status()

        j = await response.json()
        return [Efaktura(efaktura_data, self.auth) for efaktura_data in j["items"]]
