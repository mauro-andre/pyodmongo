from pyodmongo import AsyncDbEngine, DbModel, DbResponse
from typing import ClassVar
import asyncio

engine = AsyncDbEngine(mongo_uri="mongodb://localhost:27017", db_name="my_db")


class Product(DbModel):
    name: str
    price: float
    is_available: bool
    _collection: ClassVar = "products"


async def main():
    query = Product.name == "Box"

    response: DbResponse = await engine.delete(
        Model=Product, query=query, delete_one=True
    )


asyncio.run(main())
