from pyodmongo import DbEngine, MainBaseModel, DbModel
from typing import ClassVar
from pyodmongo.queries import elem_match

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(MainBaseModel):
    name: str
    price: float
    is_available: bool


class Order(DbModel):
    code: str
    products: list[Product]
    _collection: ClassVar = "orders"


query = elem_match(Product.name == "Box", Product.price == 50, field=Order.products)
box: Product = engine.find_one(Model=Product, query=query)
