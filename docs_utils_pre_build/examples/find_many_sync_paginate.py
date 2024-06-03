from pyodmongo import DbEngine, DbModel, ResponsePaginate
from typing import ClassVar

engine = DbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


query = (Product.price >= 50) & (Product.price < 100)

response: ResponsePaginate = engine.find_many(
    Model=Product, query=query, paginate=True, current_page=2, docs_per_page=100
)
