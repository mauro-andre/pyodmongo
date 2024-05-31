from pyodmongo import DbModel, MainBaseModel
from typing import ClassVar


class Address(MainBaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class User(DbModel):
    username: str
    password: str
    address: Address
    _collection: ClassVar = "users"
