from pyodmongo import DbModel
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import ClassVar


class Product(DbModel):
    name: str
    code: str
    description: str
    price: float
    product_type: str
    is_available: bool
    _collection: ClassVar = "products"
    _indexes: ClassVar = [
        IndexModel([("name", ASCENDING), ("price", DESCENDING)], name="name_and_price"),
        IndexModel([("product_type", DESCENDING)], name="product_type"),
    ]
