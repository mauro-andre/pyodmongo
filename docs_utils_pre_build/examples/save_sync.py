from pyodmongo import DbEngine, DbModel, DbResponse
from typing import ClassVar

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


box = Product(name="Box", price="5.99", is_available=True)

response: DbResponse = engine.save(box)
