import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from beanie import Document, Indexed, init_beanie

client = AsyncIOMotorClient("mongodb:/localhost:27017")


class Category(BaseModel):
    name: str
    description: str

    class Settings:
        name = "categories"


class Product(Document):
    name: str                          # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(float)              # You can also specify that a field should correspond to an index
    category: Category

    class Settings:
        name = "products"
