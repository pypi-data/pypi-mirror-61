import json

from typing import Optional, Union, Callable, Dict

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError, BackendApplicationClient
from aiohttp import ClientSession, ClientResponse

from .const import API_ROOT, AUTH_ROOT


class Auth:
    """ Class for making authenticated requests """

    def __init__(
        self,
        websession: ClientSession,
        customer_id: str = None,
        client_id: str = None,
        client_secret: str = None,
    ):
        self.websession = websession
        self.customer_id = customer_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    async def async_get_access_token(self) -> str:
        """ Return a valid access token """
        if self.token is None:
            oauth2_client = BackendApplicationClient(client_id=self.client_id)
            session = OAuth2Session(client=oauth2_client)
            self.token = session.fetch_token(
                token_url=f"{AUTH_ROOT}/identityserver/connect/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            self.websession.access_token = self.token

        return self.token["access_token"]

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """ Make a request """
        headers = kwargs.get("headers")

        if headers is None:
            headers = {"customerId": self.customer_id}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, f"{API_ROOT}/{url}", **kwargs, headers=headers
        )
