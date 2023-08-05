# sbanken-api

A Python package for communicating with the Sbanken API. Updated to work with latest version of Sbanken's API.

Forked from https://github.com/Lilleengen/sbanken-python

A lot of the code in this packages comes from or is based on code from Sbanken's official example code at https://github.com/Sbanken/api-examples/tree/master/PythonSampleApplication

## Authentication

The library can only access your own data and accounts. In order to do this you need to be authenticated.

Sbanken uses the OAuth2 standard for authentication.

To get your client_id and secret password for the API, you need to log in to your account in Sbanken. Then go to https://sbanken.no/bruke/utviklerportalen/ and enable 'Beta features'. Once that's done you should be able to obtain your personal client_id and secret.

customer_id is your full social security number (Norwegian: fødsels- og personnummer).

Currently, this library is read only, meaning it can only read data from your account. Sbanken's API does however support transferring money between your own accounts, and the library will support that in a later version.

## Currently implemented features

- Get information about all accounts, or one specific account
- Get information about recently committed transactions
- Get information about eFakturas (electronic bills)

## Example usage

```python
import asyncio
import aiohttp
from sbanken import Auth, SbankenAPI

async def main():
    async with aiohttp.ClientSession() as session:
        client = SbankenAPI(session, "customer_id", "client_id", "secret")

        accounts = await api.async_get_accounts()
        for account in accounts:
            print(f"Account name: {account.name}")
            print(f"Balance: {account.balance")

asyncio.run(main())
```
