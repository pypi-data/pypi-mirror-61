# sbanken-api

A Python package for communicating with the Sbanken API. Updated to work with latest version of Sbanken's API.

Forked from https://github.com/Lilleengen/sbanken-python

A lot of the code in this packages comes from or is based on code from Sbanken's official example code at https://github.com/Sbanken/api-examples/tree/master/PythonSampleApplication

## Usage

```python
from sbanken import SbankenAPI

client = SbankenAPI("customer_id", "client_id", "secret")

print(client.get_accounts())
print(client.get_customer_information())
print(client.get_account("account_id"))
print(client.get_transactions("account_id"))
print(client.get_cards())
print(client.get_efakturas())
print(client.get_payments("account_id"))

client.transfer(
    "fromAccountId",
    "toAccountId",
    1.0,              # amount
    "Message",
)
```
