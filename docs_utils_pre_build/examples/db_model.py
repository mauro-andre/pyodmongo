from pyodmongo import DbModel
from typing import ClassVar


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"
