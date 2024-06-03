from pyodmongo import DbEngine, DbModel
from typing import ClassVar
from pyodmongo.queries import and_, gt, lte

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


query = and_(gt(Product.price, 10), lte(Product.price, 50))
box: Product = engine.find_one(Model=Product, query=query)
