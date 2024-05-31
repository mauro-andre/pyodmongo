from pyodmongo import DbModel
from pydantic import BaseModel
from typing import ClassVar


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class User(DbModel):
    username: str
    password: str
    address: Address
    _collection: ClassVar = "users"
