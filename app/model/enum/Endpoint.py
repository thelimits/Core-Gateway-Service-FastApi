from enum import Enum

class Endpoint(Enum):
    CUSTOMERS = "/v1/customers"
    ACCOUNTS_V2 = "/v2/accounts"
    ACCOUNTS_V1 = "/v1/accounts"
