from pyodmongo import DbModel, Id
from typing import ClassVar


class User(DbModel):
    username: str
    password: str
    _collection: ClassVar = "users"


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    user: User | Id
    _collection: ClassVar = "products"
