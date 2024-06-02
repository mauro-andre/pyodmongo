from pyodmongo import DbEngine, DbModel
from typing import ClassVar
from pyodmongo.queries import or_, eq

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


query = or_(eq(Product.name, "Box"), eq(Product.price, 100))
box: Product = engine.find_one(Model=Product, query=query)
