from pyodmongo import AsyncDbEngine, DbModel
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


async def main():
    query = (Product.price >= 50) & (Product.price < 100)

    products: list[Product] = await engine.find_many(Model=Product, query=query)


asyncio.run(main())
