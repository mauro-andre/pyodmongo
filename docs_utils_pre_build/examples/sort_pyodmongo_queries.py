from pyodmongo import DbEngine, DbModel
from typing import ClassVar
from pyodmongo.queries import sort

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


query = Product.price >= 10
my_sort = sort((Product.name, 1), (Product.price, -1))
box: Product = engine.find_one(Model=Product, query=query, sort=my_sort)
