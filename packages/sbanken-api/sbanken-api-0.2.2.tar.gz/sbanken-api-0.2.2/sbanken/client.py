from oauthlib.oauth2 import BackendApplicationClient
import requests
from requests_oauthlib import OAuth2Session
import urllib.parse
import json


class SbankenAPI:
    api_root = "https://api.sbanken.no"

    def __init__(self, customer_id, client_id, secret):
        self.customer_id = customer_id
        self.client_id = client_id
        self.secret = secret
        self.http_session = self.create_authenticated_http_session(
            self.client_id, self.secret
        )

    def create_authenticated_http_session(
        self, client_id, client_secret
    ) -> requests.Session:
        oauth2_client = BackendApplicationClient(
            client_id=urllib.parse.quote(client_id)
        )
        session = OAuth2Session(client=oauth2_client)
        session.fetch_token(
            token_url="https://auth.sbanken.no/identityserver/connect/token",
            client_id=urllib.parse.quote(client_id),
            client_secret=urllib.parse.quote(client_secret),
        )
        return session

    def get_customer_information(self):
        response = self.http_session.get(
            self.api_root + "/exec.customers/api/v1/customers",
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["item"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_accounts(self):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/accounts",
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["items"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_account(self, account_id):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/accounts/" + account_id,
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["item"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_transactions(self, account_id):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/transactions/" + account_id,
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["items"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_cards(self):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/cards/",
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["items"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_efakturas(self):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/efakturas/",
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["items"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def get_payments(self, account_id):
        response = self.http_session.get(
            self.api_root + "/exec.bank/api/v1/payments/" + account_id,
            headers={"customerId": self.customer_id},
        ).json()

        if not response["isError"]:
            return response["items"]
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )

    def transfer(self, fromAccountId, toAccountId, amount, message):
        payload = {
            "fromAccountId": fromAccountId,
            "toAccountId": toAccountId,
            "amount": amount,
            "message": message,
        }

        response = self.http_session.post(
            self.api_root + "/exec.bank/api/v1/transfers/",
            headers={
                "customerId": self.customer_id,
                "Content-Type": "application/json",
            },
            json=payload,
        ).json()

        if not response["isError"]:
            return response
        else:
            raise RuntimeError(
                "{} {}".format(response["errorType"], response["errorMessage"])
            )
