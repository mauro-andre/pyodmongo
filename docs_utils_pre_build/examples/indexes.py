from pyodmongo import DbModel, Field
from typing import ClassVar


class Product(DbModel):
    name: str = Field(index=True)
    code: str = Field(index=True, unique=True)
    description: str = Field(text_index=True, default_language="english")
    price: float
    product_type: str
    is_available: bool
    _collection: ClassVar = "products"
