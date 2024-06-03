from pyodmongo import DbEngine, DbModel, DbResponse
from typing import ClassVar

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


query = Product.name == "Box"

response: DbResponse = engine.delete(Model=Product, query=query, delete_one=True)
